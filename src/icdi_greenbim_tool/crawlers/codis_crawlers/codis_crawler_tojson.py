import requests
import json
import os
import calendar
from typing import Tuple, Dict
from .codis_cookie_manager import get_valid_cookie

# --- 共用常數與設定 ---

API_URL = "https://codis.cwa.gov.tw/api/station"

# 共用的請求標頭，Cookie 將在執行時動態加入
HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://codis.cwa.gov.tw',
    'Referer': 'https://codis.cwa.gov.tw/StationData',
    'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# --- 共用輔助函式 ---

def _get_stn_type(station_id: str) -> str:
    """根據測站 ID 返回對應的測站類型"""
    if station_id.startswith('46'):
        return 'cwb'
    elif station_id.startswith('C0'):
        return 'auto_C0'
    elif station_id.startswith('C1'):
        return 'auto_C1'
    else:
        return 'agr'

def _fetch_and_save_data(payload: Dict, output_path: str) -> Tuple[bool, str]:
    """
    核心函式，負責發送請求、處理回應和儲存資料。

    Args:
        payload (Dict): 請求的負載資料。
        output_path (str): 輸出的完整檔案路徑。

    Returns:
        Tuple[bool, str]: 回傳操作是否成功及對應的訊息。
    """
    try:
        cookie_value = get_valid_cookie()
    except Exception as e:
        reason = f"取得 Cookie 失敗: {e}"
        return False, reason
    
    current_headers = HEADERS.copy()
    current_headers['Cookie'] = cookie_value
    
    try:
        response = requests.post(API_URL, headers=current_headers, data=payload)
        response.raise_for_status()
        response_data = response.json()

        if (isinstance(response_data, dict) and 'data' in response_data and 
            isinstance(response_data['data'], list) and len(response_data['data']) > 0 and
            'dts' in response_data['data'][0]):
            
            data_to_save = response_data['data'][0]['dts']
            
            if not data_to_save:
                return False, "下載成功，但內容為空"

            # 確保輸出目錄存在
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

            return True, "下載成功"
        else:
            return False, "API 回傳格式不符預期"

    except requests.exceptions.HTTPError as http_err:
        return False, f"發生 HTTP 錯誤: {http_err}"
    except json.JSONDecodeError:
        return False, "伺服器回應格式錯誤，可能是 Cookie 無效或已被阻擋"
    except requests.exceptions.RequestException as req_err:
        return False, f"發生網路錯誤: {req_err}"

# --- 主要功能函式 ---

def codis_yearly(station_id: str, year: str, output_dir: str) -> Tuple[bool, str]:  
    """下載指定測站的年度資料"""
    stn_type = _get_stn_type(station_id)
    start_date = f"{year}-01-01T00:00:00"
    end_date = f"{year}-12-31T00:00:00"
    
    payload = {
        'date': f'{start_date}.000+08:00', 
        'type': 'report_year',
        'stn_ID': station_id, 
        'stn_type': stn_type, 
        'more': '',
        'start': start_date, 
        'end': end_date, 
        'item': ''
    }
    
    output_filename = f"{year}_{station_id}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    return _fetch_and_save_data(payload, output_path)

def codis_monthly(station_id: str, setDate: str, output_dir: str) -> Tuple[bool, str]:
    """下載指定測站的月份資料"""
    try:
        year_str, month_str, _ = setDate.split('-')
        year = int(year_str)
        month = int(month_str)
    except ValueError:
        return False, "日期格式錯誤，應為 'YYYY-MM-DD'"

    stn_type = _get_stn_type(station_id)
    _, last_day = calendar.monthrange(year, month)
    
    start_date = f"{year:04d}-{month:02d}-01T00:00:00"
    end_date = f"{year:04d}-{month:02d}-{last_day:02d}T00:00:00"
    
    payload = {
        'date': f'{start_date}.000+08:00', 
        'type': 'report_month',
        'stn_ID': station_id, 
        'stn_type': stn_type, 
        'more': '',
        'start': start_date, 
        'end': end_date, 
        'item': ''
    }
    
    output_filename = f"{year:04d}{month:02d}_{station_id}.json"
    output_path = os.path.join(output_dir, output_filename)

    return _fetch_and_save_data(payload, output_path)
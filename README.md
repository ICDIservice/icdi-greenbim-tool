# ICDI GreenBIM Tool

ICDI 團隊內部工具庫，整合氣象資料爬蟲、建築能效計算與單位轉換功能。

## 開始使用

### 1. 建立虛擬環境（推薦）
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. 安裝套件
```bash
# 從 GitHub 安裝
pip install git+https://github.com/ICDIservice/icdi-greenbim-tool.git
```

## 快速使用

### 命令列工具
```bash
# 查看幫助
icdi-tool --help

# 下載月資料
icdi-tool crawl monthly 466920 2024-01-01 ./output

# 下載年資料  
icdi-tool crawl yearly 466920 2023 ./output
```

### Python 程式
```python
from icdi_greenbim_tool import codis_monthly, codis_yearly

success, message = codis_monthly("466920", "2024-01-01", "./output")
```

## 維護指令

### 更新套件
```bash
pip install --upgrade git+https://github.com/ICDIservice/icdi-greenbim-tool.git
```

### 卸載套件
```bash
pip uninstall icdi-greenbim-tool
```

### 退出虛擬環境
```bash
deactivate
```

## 專案結構
```
icdi-greenbim-tool/
├── crawlers/     # 爬蟲模組
├── energy/       # 能效計算  
└── utils/        # 工具函式
```

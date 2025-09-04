import typer
from typing_extensions import Annotated

from icdi_greenbim_tool import codis_monthly, codis_yearly

# 建立一個 Typer 應用程式實例
app = typer.Typer(help="ICDI GreenBIM Tool - 一個整合常用工具的指令行介面。")

# 建立一個子命令群組，專門用來放爬蟲相關的命令
crawl_app = typer.Typer()
app.add_typer(crawl_app, name="crawl", help="執行網路爬蟲相關任務。")


@crawl_app.command("monthly", help="下載指定氣象測站的月資料。")
def cli_codis_monthly(
    station_id: Annotated[str, typer.Option(help="氣象測站 ID，例如 '466920'。")],
    date: Annotated[str, typer.Option(help="指定下載的年月，格式為 'YYYY-MM-DD'，日期部分會被忽略。")],
    output_dir: Annotated[str, typer.Option(help="下載資料的存放目錄。")]
):
    """
    下載 CODiS 網站上指定測站的月資料。
    """
    print(f"[*] 開始下載測站 {station_id} 於 {date[:7]} 的月資料...")
    
    success, reason = codis_monthly(station_id=station_id, setDate=date, output_dir=output_dir)
    
    if success:
        print(f"[+] 成功: {reason}")
        raise typer.Exit(code=0)
    else:
        print(f"[!] 失敗: {reason}")
        raise typer.Exit(code=1)


@crawl_app.command("yearly", help="下載指定氣象測站的年資料。")
def cli_codis_yearly(
    station_id: Annotated[str, typer.Option(help="氣象測站 ID，例如 '466920'。")],
    year: Annotated[str, typer.Option(help="指定下載的年份，格式為 'YYYY'。")],
    output_dir: Annotated[str, typer.Option(help="下載資料的存放目錄。")]
):
    """
    下載 CODiS 網站上指定測站的年資料。
    """
    print(f"[*] 開始下載測站 {station_id} 於 {year} 年的資料...")
    
    success, reason = codis_yearly(station_id=station_id, year=year, output_dir=output_dir)
    
    if success:
        print(f"[+] 成功: {reason}")
        raise typer.Exit(code=0)
    else:
        print(f"[!] 失敗: {reason}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
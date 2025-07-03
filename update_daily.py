# update_daily.py
from datetime import date
import akshare as ak
import pandas as pd
from config import get_engine
from db_utils import get_stock_list_table, get_daily_table, ensure_table

def update_daily_data():
    today = date.today()
    engine = get_engine()
    stock_list = get_stock_list_table()

    with engine.connect() as conn:
        results = conn.execute(stock_list.select()).fetchall()

    for row in results:
        code = row["code"]
        print(f"更新 {code}")
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=today.strftime('%Y%m%d'))
        if df.empty:
            continue
        df = df.rename(columns={
            "日期": "date", "开盘": "open", "最高": "high", "最低": "low", "收盘": "close",
            "成交量": "volume", "成交额": "amount", "换手率": "turnover"
        })
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df[["date", "open", "high", "low", "close", "volume", "amount", "turnover"]]

        table = get_daily_table(code)
        ensure_table(engine, table)
        df.to_sql(table.name, con=engine, if_exists="append", index=False, method="multi")

        with engine.begin() as conn:
            conn.execute(
                stock_list.update().where(stock_list.c.code == code),
                {"last_update": today}
            )

if __name__ == "__main__":
    update_daily_data()

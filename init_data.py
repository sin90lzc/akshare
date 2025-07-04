# init_data.py
import sys
import akshare as ak
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from config import get_engine
from db_utils import get_stock_list_table, get_daily_table, ensure_table
import time
def fetch_and_store_stock_list(engine):
    df = ak.stock_info_a_code_name()
    df["board"] = "A股"
    df["list_date"] = datetime.today().date()
    df["last_update"] = None

    stock_list = get_stock_list_table()
    ensure_table(engine, stock_list)

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                stock_list.insert().prefix_with("IGNORE"),
                dict(
                    code=row["code"],
                    name=row["name"],
                    board=row["board"],
                    list_date=row["list_date"],
                    last_update=None
                )
            )
    return df["code"].tolist()

def fetch_daily_data(code, start_date):
    df = ak.stock_zh_a_hist(symbol=code, start_date=start_date.strftime('%Y%m%d'), adjust="")
    time.sleep(3)  # 避免请求过快导致被限制
    df = df.rename(columns={
        "日期": "date", "开盘": "open", "最高": "high", "最低": "low", "收盘": "close",
        "成交量": "volume", "成交额": "amount", "换手率": "turnover"
    })
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df[["date", "open", "high", "low", "close", "volume", "amount", "turnover"]]

def init_all_stocks(start_date):
    engine = get_engine()
    stock_codes = fetch_and_store_stock_list(engine)

    for code in stock_codes:
        try:
            code_num = int(code)
            if code_num <= 2568:
                continue
        except ValueError:
            continue
            
        print(f"初始化 {code}")
        df = fetch_daily_data(code, start_date)
        table = get_daily_table(code)
        ensure_table(engine, table)
        # 分批处理数据，每1000条一批
        batch_size = 1000
        total_batches = (len(df) // batch_size) + 1
        for i in range(total_batches):
            start = i * batch_size
            end = (i + 1) * batch_size
            batch = df[start:end]
            if not batch.empty:
                batch.to_sql(table.name, con=engine, if_exists="append", index=False, method="multi")
                print(f"已写入批次 {i+1}/{total_batches} ({len(batch)}条记录)")

        with engine.begin() as conn:
            stock_list = get_stock_list_table()
            conn.execute(
                stock_list.update().where(stock_list.c.code == code),
                {"last_update": df["date"].max()}
            )

if __name__ == "__main__":
    import pandas as pd
    if len(sys.argv) != 2:
        print("Usage: python init_data.py YYYY-MM-DD")
        sys.exit(1)

    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    init_all_stocks(start_date)

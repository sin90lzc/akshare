# db_utils.py
from sqlalchemy import Column, String, Float, Date, BigInteger, Table, MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine import Engine

metadata = MetaData()

def get_stock_list_table():
    return Table(
        "stock_list", metadata,
        Column("code", String(10), primary_key=True),
        Column("name", String(100)),
        Column("board", String(50)),
        Column("list_date", Date),
        Column("last_update", Date, nullable=True)
    )

def get_daily_table(stock_code: str):
    return Table(
        f"daily_{stock_code}", metadata,
        Column("date", Date, primary_key=True),
        Column("open", Float),
        Column("high", Float),
        Column("low", Float),
        Column("close", Float),
        Column("volume", BigInteger),
        Column("amount", Float),
        Column("turnover", Float)
    )

def ensure_table(engine: Engine, table: Table):
    metadata.bind = engine
    try:
        table.create(checkfirst=True)
    except ProgrammingError as e:
        print(f"Error creating table {table.name}: {e}")

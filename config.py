# config.py
DB_USER = "admin"
DB_PASSWORD = "mm753951"
DB_HOST = "mariadb"
DB_PORT = 3306
DB_NAME = "akshare"

from sqlalchemy import create_engine

def get_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    return create_engine(url, echo=False, pool_recycle=3600)

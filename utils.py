import os

from dotenv import load_dotenv


def load_db_config():
    """
    連線到資料庫。
    """

    load_dotenv()
    return {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_db_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
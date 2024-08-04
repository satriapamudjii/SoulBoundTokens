from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    db_session = SessionLocal()
    try:
        yield db_session
    except exc.DBAPIError as e:
        if e.connection_invalidated:
            print("Database connection was invalidated!")
        else:
            print("Database error:", e)
    except exc.SQLAlchemyError as e:
        print("An error occurred with SQLAlchemy:", e)
    finally:
        db_session.close()
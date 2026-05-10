from sqlalchemy import create_engine
# create engine -> is used to establish connection between database and this file

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

# read variables
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

print(MYSQL_USER)  # debug

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print(DATABASE_URL)

# Connection
engine = create_engine(DATABASE_URL)

# Session
# 1. Define the factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Create a dependency
def get_db():
    db = SessionLocal()
    try:
        yield db # stops the session
    finally:
        db.close() # Always close the connection to avoid leaking memory


# Base
Base = declarative_base()


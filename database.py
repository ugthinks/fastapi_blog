##database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
# url tells where to connect, sqlite
# . is current directory
# blog.db will automaticaaly be changed
# when we will switch to postgre changing the url only is enough
#Think of SQLite as the filing cabinet and SQLAlchemy as the organized assistant that handles the filing.

engine = create_engine (
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
#sqlite uses True to check same thread as default it checks is that was created by you 
# if not you are not allowed to access the file (A security guard)


SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)
# This is a factory that creates sessions
# A session is essentially a transaction with DataBase
# Each request gets its own session
# Auto commit = False, Auto Flush = False -> We want to control when to commit


class Base (DeclarativeBase):
    pass
# DeclarativeBase is a factory that knows how to create database tables.
# It already contains a huge amount of SQLAlchemy code.
# Your Base inherits all of SQLAlchemy's functionality.


def get_db():
    with SessionLocal() as db:
        yield db
# SessionLocal A machine that creates database sessions. using 'with' closes the sessions automatically
# if we have used return to open session then we caan't come back to close file using 'with'.

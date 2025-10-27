from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeBase


Base: DeclarativeBase = declarative_base()

engine = create_engine('sqlite:///database/psychology_bot.db', echo=True)
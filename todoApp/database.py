#instll sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy. orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
#for postgre SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost/TodoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test1234!@127.0.0.1:3306/TodoApllicationDatabase'

''''''#for sqllite only     , , , , , engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}'''
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit =False, autoflush = False , bind = engine)

Base = declarative_base()





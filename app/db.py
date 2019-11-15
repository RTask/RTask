from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = 'postgresql://RobedCoder:RobedCoder@localhost:5432/rtask' # move to config 
engine = create_engine(db_url)
Base = declarative_base()
db_session = sessionmaker(bind=engine)

# import models after base is declared
from models import ticket
from models import status
from models import message

def init_db():
    try:
        print('checking database and table status')
        Base.metadata.create_all(engine)
        print('tables exist')
    except Exception as ex:
        print(ex)    


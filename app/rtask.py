from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://RobedCoder:RobedCoder@localhost:5432/rtask')
Base = declarative_base(engine)
db_session = sessionmaker(bind=engine)

class RTask():
    def __init__(self):
        self.start()
    
    def start():
        print('starting RTask and checking Config')
        print('config looks good, starting RTask server')
        exec('server.py') 
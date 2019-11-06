import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from wtforms_alchemy import ModelForm
from wtforms import SubmitField

engine = create_engine('postgresql://postgres:RobedCoder@localhost:5432/rtask')
Base = declarative_base(engine)
db_session = sessionmaker(bind=engine)

class Ticket(Base):
    __tablename__ = 'ticket'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    title = sa.Column(sa.Unicode(100), nullable=False)
    description = sa.Column(sa.Unicode(255), nullable=False)

    
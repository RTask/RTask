import sqlalchemy as sa
from db import Base

class Message(Base):
    
    def __init__(self, title, description, userId, sentBy, sentTo):
        self.title = title
        self.description = description
        self.userId = userId
        self.sentBy = sentBy
        self.sentTo = sentTo 

    __tablename__ = 'messages'

    # primary key of message
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    # the title of the message
    title = sa.Column(sa.Unicode(100), nullable=False)
    description = sa.Column(sa.Unicode(500), nullable=False)
    # user who created the message
    userId = sa.Column(sa.String(50), nullable=False)
    # userId of who sent the message
    sentBy = sa.Column(sa.String(50), nullable=False)
    # userId of who is to receive the message
    sentTo = sa.Column(sa.String(50), nullable=False)
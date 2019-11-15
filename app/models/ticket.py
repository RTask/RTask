import sqlalchemy as sa
from sqlalchemy.orm import relationship
from db import Base

class Ticket(Base):
    
    __tablename__ = 'ticket'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    title = sa.Column(sa.Unicode(100), nullable=False)
    description = sa.Column(sa.Unicode(255), nullable=False)
    userId = sa.Column(sa.String(50), nullable=False)
    statusId = sa.Column(sa.BigInteger, sa.ForeignKey('status.id'))
    status = relationship("Status")
   

    



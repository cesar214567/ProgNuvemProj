from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from database import connector

class Tweet(connector.Manager.Base):
    __tablename__='tweet'
    id = Column(Integer,primary_key=True,autoincrement=True)
    text =Column(String(50))
    date = Column(DateTime)
    
db = connector.Manager()
engine = db.createEngine()
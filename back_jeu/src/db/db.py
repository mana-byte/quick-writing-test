from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Performance(Base):
    __tablename__ = "performance"  # Table name in the database
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time_taken = Column(Integer) # in milliseconds

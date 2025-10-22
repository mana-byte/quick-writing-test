from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Performance
import os

db_url = os.environ.get("DATABASE_URL", "postgresql+psycopg2://mana:pswd@db:8878/pg_db")
# Create a connection string
engine = create_engine(db_url)

connection = engine.connect()

Base.metadata.create_all(engine) # create all tables

Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the employees table
performance_base = Performance(name="Manaiki", time_taken=60*1000)
session.add(performance_base)
session.commit()

print("Data inserted successfully.")

# Test the connection
connection.close()

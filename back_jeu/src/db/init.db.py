from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Performance

# Create a connection string
engine = create_engine('postgresql+psycopg2://mana:pswd@localhost:8898/pg_db')

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

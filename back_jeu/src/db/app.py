from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db import Performance
import os

db_url = os.environ.get("DATABASE_URL", "postgresql+psycopg2://mana:pswd@db:8878/pg_db")

def get_db():
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session # Use yield to make this a generator
    finally:
        session.close()


def add_performance(session, name: str, time_taken: int):
    performance = Performance(name=name, time_taken=time_taken)
    session.add(performance)
    session.commit()
    session.refresh(performance)
    return performance


def get_performances(session):
    return session.query(Performance).all()


def remove_performance(session, performance_id: int):
    performance = (
        session.query(Performance).filter(Performance.id == performance_id).first()
    )
    if performance:
        session.delete(performance)
        session.commit()
        return True
    return False


def update_performance(
    session, performance_id: int, name: str = "Manaiki", time_taken: int = 1
):
    performance = (
        session.query(Performance).filter(Performance.id == performance_id).first()
    )
    if performance:
        if name:
            performance.name = name
        if time_taken:
            performance.time_taken = time_taken
        session.commit()
        session.refresh(performance)
        return performance
    return None

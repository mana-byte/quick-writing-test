from operator import concat
from httpx import get
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db import Performance
import os
from contextlib import contextmanager

db_url = os.environ.get("DATABASE_URL", "postgresql+psycopg2://mana:pswd@db:8878/pg_db")

@contextmanager
def get_db():
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session # Use yield to make this a generator
    finally:
        session.close()
        print("[INFO]: Database session closed.")


def add_performance(name: str, time_taken: int):
    with get_db() as session:
        performance = Performance(name=name, time_taken=time_taken)
        session.add(performance)
        session.commit()
        session.refresh(performance)
        return performance


def get_performances():
    with get_db() as session:
        return session.query(Performance).all()


def remove_performance(performance_id: int):
    with get_db () as session:
        performance = (
            session.query(Performance).filter(Performance.id == performance_id).first()
        )
        if performance:
            session.delete(performance)
            session.commit()
            return True
        return False


def update_performance(
    performance_id: int, name: str = "Manaiki", time_taken: int = 1
):
    with get_db() as session:
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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Подключаем существующую базу students.db
DATABASE_URL = "sqlite:///students.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

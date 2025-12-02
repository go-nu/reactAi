from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

DB_URL = "postgresql+psycopg2://kogo:math1106@localhost:5433/mydb"
engine: Engine = create_engine(DB_URL, echo=False, future=True)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# backend/db/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# backend/.env 자동 로딩
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL 환경변수가 없습니다. backend/.env를 확인하세요.")

engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

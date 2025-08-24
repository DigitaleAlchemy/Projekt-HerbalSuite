
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import yaml

load_dotenv()

Base = declarative_base()


def _load_cfg():
    path = os.environ.get('HERBALSUITE_CONFIG', '') or os.path.join(os.path.dirname(__file__), '..', 'config', 'default.yml')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

_cfg = _load_cfg()
DATABASE_URL = os.environ.get('DATABASE_URL') or _cfg.get('database', {}).get('url') or 'sqlite+pysqlite:///:memory:'

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

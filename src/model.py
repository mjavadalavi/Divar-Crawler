import os
from pathlib import Path

from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import (
    Column,
    Integer,
    Text,
    create_engine
)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()}/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    , pool_size=10, max_overflow=20
)

Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


class Ads(Base):
    __tablename__ = 'ads'
    id = Column(Integer(), primary_key=True)
    hash_code = Column(Text, nullable=True, unique=False)
    chat_id = Column(Text, nullable=True, unique=False)


Base.metadata.create_all(engine)

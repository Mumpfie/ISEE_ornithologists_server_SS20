from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://app_user:app_user@localhost:3306/ornithologists"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL ,
    connect_args={"check_same_thread": False} # TODO: only needed for mysql
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
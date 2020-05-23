import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.environ.get('DB_USER')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')
db_name  = os.environ.get('DB_NAME')

if db_user is None or db_host is None or db_port is None or db_password is None or db_name is None:
    raise EnvironmentError('DB config missing. Environment variable undefined.')

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://" + db_user + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name

picture_dir = '/pictures'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
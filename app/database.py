from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@postgres_server/<database>'
SQLALCHEMY_DATABASE_URL = 'postgresql://root:root@localhost/fastapi_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency for sqlalchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
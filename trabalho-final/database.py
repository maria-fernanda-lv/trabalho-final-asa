from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# BANCO ========================================================
# Configuração da URL do PostgreSQL
db_url = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='1989',
    host='localhost',
    database='trabalho_final',
    port=5432
)

# Configuração da conexão com o PostgreSQL
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = Session()  # Assuming SessionLocal is your database session factory
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(engine)
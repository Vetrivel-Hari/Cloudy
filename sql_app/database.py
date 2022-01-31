import imp
from lib2to3.pytree import Base
from pkgutil import ImpImporter
from threading import local
from turtle import end_fill
from django.template import engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/Cloudy"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size = 100, max_overflow = 0)

localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
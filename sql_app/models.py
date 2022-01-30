from fileinput import filename
from os import link
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, null

from .database import Base

class loginDetails(Base):
    __tablename__ = "logindetails"

    uid = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

class fileDetails(Base):
    __tablename__ = "filedetails"

    fileid = Column(Integer, primary_key=True)
    filename = Column(String)
    filelink = Column(String)
    links = Column(Integer)   

class fileOwner(Base):
    __tablename__ = "fileowner"

    ownerid = Column(Integer, ForeignKey('logindetails.uid'), primary_key=True)
    fileid = Column(Integer, ForeignKey('filedetails.fileid'), primary_key=True)

class sharedFiles(Base):
    __tablename__ = "sharedfiles"

    filefrom = Column(Integer, ForeignKey('logindetails.uid'), primary_key=True)
    fileto = Column(Integer, ForeignKey('logindetails.uid'), primary_key=True)
    fileid = Column(Integer, ForeignKey('filedetails.fileid'), primary_key=True)
    filename = Column(String)

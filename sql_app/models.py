from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, null

from .database import Base

class loginDetails(Base):
    __tablename__ = "logindetails"

    uid = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    
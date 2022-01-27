from typing import List, Optional
from pydantic import BaseModel

class loginDetailsBase(BaseModel):
    username: str
    fullname: str

class loginDetailsCreate(loginDetailsBase):
    password: str

    class Config:
        orm_mode = True

class loginDetailsRead(loginDetailsBase):
    uid: int
    disabled: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class fileDetails(BaseModel):
    fileid: int
    filename: str
    filelink: str
    link: int

    class Config:
        orm_mode = True

class fileOwner(BaseModel):
    ownerid: int
    fileid: int

    class Config:
        orm_mode = True


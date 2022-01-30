from datetime import datetime, timedelta
from distutils import extension
from fileinput import filename
import imp
from operator import mod
import os
import magic
import shutil
from typing import List, Optional
from urllib.request import Request

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from isort import file
from jose import JWTError, jwt
from matplotlib import image
from numpy import delete
from passlib.context import CryptContext
from pydantic import BaseModel, FilePath
from starlette.responses import FileResponse

from sql_app import models, schemas
from sql_app.database import localSession, engine
from sqlalchemy.sql.expression import func
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import delete, and_

SECRET_KEY = "fc364310651db317ac759b29594b6af12ec1a1534d41177a00b640f6dbb8139d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

'''
As backend and frontend are running on the same machine and browser
google chrome and firefox are blocking the fetch() request stating that
CORS (Cross-Origin Resource Sharing)
so we need to allow CORS

Refer: https://fastapi.tiangolo.com/tutorial/cors/

Open the client side HTML after starting the python -m http.server 500
in that required folder
'''

app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Dependency
def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_create(userName: str):
    db_user = localSession().query(models.loginDetails).filter(models.loginDetails.username == userName).first()

    #print(type(db))
    #Check - 1
    if (db_user):
        data = schemas.loginDetailsCreate(username=db_user.username, fullname=db_user.fullname, password=db_user.password)
        return data

def get_user_read(userName: str):
    db_user = localSession().query(models.loginDetails).filter(models.loginDetails.username == userName).first()

    #print(type(db))
    #Check - 1
    if (db_user):
        b =  False if (str(db_user.disabled) == "false") else True
        data = schemas.loginDetailsRead(uid = int(db_user.uid),username=db_user.username, fullname=db_user.fullname, disabled=b)
        return data

def authenticate_user(username: str, password: str):
    user = get_user_create(username)

    if(not user):
        return False
    
    if(not verify_password(password, user.password)):
        return False

    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if (expires_delta):
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("id")

        if (username is None):
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_read(userName=token_data.username)

    if(user is None):
        raise credentials_exception

    return user

async def get_current_active_user(current_user: schemas.loginDetailsRead = Depends(get_current_user)):
    if(not current_user.disabled):
        raise HTTPException(status_code = 400, detail="Inactive User")

    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(formData: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(formData.username, formData.password)

    if(not user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate" : "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data = {"id" : user.username}, expires_delta=access_token_expires
    )

    return {"access_token" : access_token, "token_type" : "bearer"}

@app.post("/signup", response_model=schemas.loginDetailsRead)
def create_user(user: schemas.loginDetailsCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.loginDetails).filter(models.loginDetails.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashedPassword = get_password_hash(user.password)

    t = db.query(func.max(models.loginDetails.uid)).scalar()

    if t == None:
        t = 0

    t = int(t) + 1

    db_user = models.loginDetails(uid = t, username = user.username, fullname = user.fullname, password = hashedPassword, disabled = False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users/me", response_model=schemas.loginDetailsRead)
async def read_users_me(current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    return current_user
    
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...),current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    mydir = ("./userFiles/" + str(current_user.uid))
    
    checkFolder = os.path.isdir(mydir)

    if(not checkFolder):
        os.makedirs(mydir)

    filePath = "./userFiles/" + str(current_user.uid)+ "/" + file.filename

    file_exists = os.path.exists(filePath)
    
    if(not file_exists):
        t = localSession().query(func.max(models.fileDetails.fileid)).scalar()

        if t == None:
            t = 0

        t = int(t) + 1

        #INSERTING INTO THE FILEDETAILS TABLE
        db_user = models.fileDetails(fileid = int(t), filename = file.filename, filelink = filePath, links = 1)
        
        db = localSession()

        db.add(db_user)
        db.commit()


        #INSERTING INTO THE FILEOWNER TABLE
        db_user = models.fileOwner(ownerid = current_user.uid, fileid = int(t))
        
        db = localSession()

        db.add(db_user)
        db.commit()

        with open(filePath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"filename" : file.filename}
    else:
        return HTTPException(status_code=400, detail="File already exists")

def getFilesofReciver(toUser):
    t = localSession().query(models.fileOwner).filter(models.fileOwner.ownerid == toUser).all()

    l = []
    for i in t:
        l.append(int(i.fileid))

    t = localSession().query(models.sharedFiles).filter(models.sharedFiles.fileto == toUser).all()
    
    for i in t:
        l.append(int(i.fileid))

    return l


@app.get("/sharefiles")
def shareFiles(fileid: int, toUser: str, current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    db = localSession()
    
    t = localSession().query(models.fileOwner).filter(models.fileOwner.ownerid == current_user.uid).all()

    l = []
    for i in t:
        l.append(int(i.fileid))

    t = localSession().query(models.sharedFiles).filter(models.sharedFiles.fileto == current_user.uid).all()
    
    for i in t:
        l.append(int(i.fileid))

    t = db.query(models.loginDetails).filter(models.loginDetails.username == toUser).count()

    if(t > 0):
        if(fileid in l):
            t = db.query(models.loginDetails).filter(models.loginDetails.username == toUser).first()
            fileto = int(t.uid)
            filefrom = int(current_user.uid)
            
            x = getFilesofReciver(fileto)
            if(fileid not in x):
                t = db.query(models.fileDetails).filter(models.fileDetails.fileid == fileid).first()
                t.links = t.links + 1

                orginalFilename = t.filelink[str(t.filelink).rindex("/")+1:]

                db.commit()

                db_user = models.sharedFiles(filefrom = filefrom, fileto = fileto, fileid = fileid, filename = orginalFilename)
                db.add(db_user)
                db.commit()

                return {"Details": "Success"}
            else:
                return HTTPException(status_code=402, detail="The receiver already has that file")
        else:
            return HTTPException(status_code=400, detail="You don't have access to that file")
    else:
        return HTTPException(status_code=401, detail="No such User is Available")

@app.get("/getfiles")
async def getfiles(current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    t = localSession().query(models.fileOwner).filter(models.fileOwner.ownerid == current_user.uid).all()

    d = {}

    l = []
    for i in t:
        l.append(i.fileid)

    l = tuple(l)

    t = localSession().query(models.fileDetails).filter(models.fileDetails.fileid.in_(l)).all()
    
    ownedfiles = {}
    for i in t:
        ownedfiles[i.fileid] = i.filename

    d["ownedfiles"] = ownedfiles

    t = localSession().query(models.sharedFiles).filter(models.sharedFiles.fileto == current_user.uid).all()

    l = []
    for i in t:
        l.append(i.fileid)

    l = tuple(l)

    t = localSession().query(models.sharedFiles).filter(models.sharedFiles.fileid.in_(l)).all()
    
    sharedfiles = {}
    for i in t:
        if(i.fileto == current_user.uid):
            sharedfiles[i.fileid] = i.filename

    d["sharedfiles"] = sharedfiles

    return d

@app.get("/renamefile")
def renameFile(fileid: int, newName: str, current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    db = localSession()
    
    t = localSession().query(models.fileOwner).filter(models.fileOwner.ownerid == current_user.uid).all()

    owner = []
    for i in t:
        owner.append(int(i.fileid))

    t = localSession().query(models.sharedFiles).filter(models.sharedFiles.fileto == current_user.uid).all()
    
    shared = []
    for i in t:
        shared.append(int(i.fileid))

    if(fileid in owner):
        t = db.query(models.fileDetails).filter(models.fileDetails.fileid == fileid).first()
        oldPath = t.filelink
        
        newPath = oldPath[:oldPath.rindex("/")+1] + newName + oldPath[oldPath.rindex("."):]
        t.filelink = newPath
        t.filename = newName + oldPath[oldPath.rindex("."):]
        db.commit()

        os.rename(oldPath, newPath)

        return {"Details": "Success"}
    elif (fileid in shared):
        t = db.query(models.sharedFiles).filter(models.sharedFiles.fileid == fileid).all()

        for i in t:
            if(i.fileto == current_user.uid):
                oldName = str(i.filename)
                extension = oldName[oldName.rindex("."):]
                i.filename = newName + extension

        db.commit()
        return {"Details": "Success"}
    else:
         return HTTPException(status_code=400, detail="You don't have access to that file")

@app.get("/deletefile")
def renameFile(fileid: int, current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    db = localSession()
    globalLink = -1

    t = localSession().query(models.fileOwner).filter(models.fileOwner.ownerid == current_user.uid).all()

    owner = []
    for i in t:
        owner.append(int(i.fileid))

    t = localSession().query(models.sharedFiles).filter(models.sharedFiles.fileto == current_user.uid).all()
    
    shared = []
    for i in t:
        shared.append(int(i.fileid))

    if(fileid in owner):
        t = db.query(models.fileOwner).filter(and_(models.fileOwner.ownerid == current_user.uid, models.fileOwner.fileid == fileid)).delete()
        db.commit()

        t = db.query(models.fileDetails).filter(models.fileDetails.fileid == fileid).first()
        t.links = t.links - 1
        globalLink = t.links

        db.commit()
    elif (fileid in shared):
        t = db.query(models.sharedFiles).filter(and_(models.sharedFiles.fileto == current_user.uid, models.sharedFiles.fileid == fileid)).delete()
        db.commit()

        t = db.query(models.fileDetails).filter(models.fileDetails.fileid == fileid).first()
        t.links = t.links - 1
        globalLink = t.links
        db.commit()
    else:
         return HTTPException(status_code=400, detail="You don't have access to that file")

    if(globalLink == 0):
        t = db.query(models.fileDetails).filter(models.fileDetails.fileid == fileid).first()
        filePath = str(t.filelink)

        os.remove(filePath)

        t = db.query(models.fileDetails).filter(models.fileDetails.fileid == fileid).delete()
        db.commit()

    return {"Details": "Success"}

@app.get("/downloadfile", response_class=FileResponse)
def downloadFile():
    mime = magic.Magic(mime=True)
    x = mime.from_file("./userFiles/1/Brochure.pdf")
    
    file_location = "./userFiles/1/Brochure.pdf"

    return FileResponse(file_location, media_type=x,filename="Brochure")


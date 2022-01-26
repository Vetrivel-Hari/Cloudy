from faulthandler import disable
from pyexpat import model
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import models, schemas
from sql_app.database import localSession, engine
from sqlalchemy.sql.expression import func


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.loginDetailsRead)
def create_user(user: schemas.loginDetailsCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.loginDetails).filter(models.loginDetails.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashedPassword = user.password

    t = db.query(func.max(models.loginDetails.uid)).scalar()

    if t == None:
        t = 0

    t = int(t) + 1

    db_user = models.loginDetails(uid = t, username = user.username, fullname = user.fullname, password = user.password, disabled = False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


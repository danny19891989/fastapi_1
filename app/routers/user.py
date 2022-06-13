from typing import List
from .. import models, schemas, utils
from fastapi import status, HTTPException, Response, Depends, APIRouter

from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def Create_User(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

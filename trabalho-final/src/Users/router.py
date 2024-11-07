from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from .models import User
from .schemas import AddFundsRequest, UserCreate, UserResponse
from .auth_utils import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

# Route to sign up a new user
@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(content={"msg": "User created successfully", "user": {"username": new_user.username, "email": new_user.email}}, status_code=201)


# Route to login and get the JWT token
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return JSONResponse(content={
    "access_token": access_token,
    "token_type": "bearer"
}, status_code=200)


@router.get("/users", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    users_response = []
    for user in users:
        users_response.append(UserResponse(id=user.id, username=user.username,
                                           email=user.email, account_balance=user.account_balance))
    return users_response

@router.post("/add-funds")
async def add_money_to_account(request: AddFundsRequest, 
                               current_user: User = Depends(get_current_user), 
                               db: Session = Depends(get_db)):
    
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    current_user.account_balance += request.amount
    db.add(current_user)
    db.commit()

    return JSONResponse(content={
        "message": "Money added successfully.", 
        "new_balance": str(current_user.account_balance)}, status_code=200)


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, username=current_user.username,
                        email=current_user.email, account_balance=current_user.account_balance)
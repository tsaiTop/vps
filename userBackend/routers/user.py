from fastapi import APIRouter,Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from modal import UserModal
from utils.jwt import create_access_token
from lib.db import get_database
from lib.deps import get_current_user


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
   
    database = await get_database()
    user = database.users.find_one({"email": form_data.username})
    if not pwd_context.verify(form_data.password,user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token({
        "id": str(user["_id"]),
        "userName": user["userName"],
        "email": user["email"]
    })
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", summary="用户信息")
async def info(current_user: UserModal = Depends(get_current_user)):
    return {
        "status": "success",
        "msg": "获取用户信息成功！",
        "data": current_user
    }


@router.post("/recharge",summary="用户充值")
async def recharge(money: int,current_user: UserModal = Depends(get_current_user)):
    raise HTTPException(status_code=400, detail="寻找支付接口中！")


    
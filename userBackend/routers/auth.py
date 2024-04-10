
import time
from fastapi import APIRouter, BackgroundTasks, HTTPException,status
from passlib.context import CryptContext

from modal import UserRegisterModal, SendCodeByEmailModal, UserLoginModal
from utils.email import generate_verification_code,send_email_code
from lib.db import get_database
from lib.redis import set_value_with_expire,get_value, delete_key
from utils.jwt import create_access_token
from server.auth import validate_user_registration, validate_send_email_code

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post("/sendCode", summary="发送验证码")
async def sendCode(background_tasks: BackgroundTasks, send_email: SendCodeByEmailModal):
  await validate_send_email_code(send_email)

  emailCode = await get_value(f"verification_code:{send_email.email}")
  if not emailCode:
    emailCode = generate_verification_code()
    # 后台发送邮件
    background_tasks.add_task(send_email_code, send_email.email, emailCode)

    await set_value_with_expire(f"verification_code:{send_email.email}", emailCode, 600)
      
  return {
    "code": "success",
    "msg": "验证码发送成功！",
  }


@router.post("/register", summary="用户注册")
async def register(user_register: UserRegisterModal):
  await validate_user_registration(user_register)

  database = await get_database()
  if database.users.find_one({"email": user_register.email}):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被注册")
  
  # 删除验证码
  await delete_key(f"verification_code:{user_register.email}")
  
  hashed_password = pwd_context.hash(user_register.password)
  user_data = {
    "email": user_register.email,
    "userName": user_register.email,
    "password": hashed_password,
    "balance": 0,
    "At": int(time.time() * 1000),
  }
  result = database.users.insert_one(user_data)

  access_token = create_access_token({
    "id": str(result.inserted_id),
    "userName": user_register.email,
    "email": user_register.email
  })
  

  return {
    "status": "success",
    "msg": "注册成功！",
    "data": {
      "userName": user_register.email,
      "email": user_register.email,
      "access_token": access_token,
    }
  }


@router.post("/login", summary="用户登录")
async def login(user_login: UserLoginModal):
  
  database = await get_database()
  user = database.users.find_one({"email": user_login.email})
  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱或密码错误")
  
  if not pwd_context.verify(user_login.password, user["password"]):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱或密码错误")
  
  access_token = create_access_token({
    "id": str(user["_id"]),
    "userName": user["userName"],
    "email": user["email"]
  })
  
  return {
    "status": "success",
    "msg": "登录成功！",
    "data": {
      "userName": user["userName"],
      "email": user["email"],
      "access_token": access_token,
    }
  }
  


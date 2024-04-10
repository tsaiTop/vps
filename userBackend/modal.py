from fastapi import Depends
from pydantic import BaseModel, EmailStr, validator
from typing import Literal

from lib.deps import get_current_user

# 发送验证码
class SendCodeByEmailModal(BaseModel):
  email: EmailStr


# 用户
class UserModal(BaseModel):
    username: str
    email: EmailStr
    balance: int
    password: str
    createdAt: int
    endAt: int

# 用户注册
class UserRegisterModal(BaseModel):
  email: EmailStr
  password: str
  code: str
  
  @validator("password")
  def password_length(cls, value: str):
        if len(value) < 6:
            raise ValueError('密码不能小于6位')
        return value
    
# 用户登录
class UserLoginModal(BaseModel):
  email: EmailStr
  password: str
  
  @validator("password")
  def password_length(cls, value: str):
        if len(value) < 6:
            raise ValueError('密码不能小于6位')
        return value

# 用户充值
class UserRechargeModal(BaseModel):
  money: int

# 购买产品
class UserBuyProductModal(BaseModel):  
  id: str
  month: int
  
# 改变服务器状态
class ServerSetStatusModal(BaseModel):
  server_id: str
  status: Literal["start", "stop", "restart"]
  current_user: UserModal = Depends(get_current_user)
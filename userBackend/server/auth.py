from fastapi import HTTPException,status
from lib.redis import get_value
from modal import SendCodeByEmailModal, UserRegisterModal
from utils.email import is_valid_email

# 验证发送邮箱验证码
async def validate_send_email_code(send_email: SendCodeByEmailModal):
  print(send_email)
  if send_email.email is None:
    raise HTTPException(status_code=400, detail="邮箱不能为空")
  if not is_valid_email(send_email.email):
    raise HTTPException(status_code=400, detail="邮箱格式不正确")

# 验证用户注册
async def validate_user_registration(user: UserRegisterModal):

  if not is_valid_email(user.email):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱格式不正确")
  if await get_value(f"verification_code:{user.email}") != user.code:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码不正确")
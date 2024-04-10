from fastapi import APIRouter, Depends

from lib.deps import get_current_user
from . import auth,user,product,servers

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(servers.router, prefix="/servers", tags=["servers"], dependencies=[Depends(get_current_user)])
api_router.include_router(product.router, prefix="/product", tags=["product"], dependencies=[Depends(get_current_user)])
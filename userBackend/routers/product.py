import time
from bson.objectid import ObjectId
from fastapi import APIRouter,BackgroundTasks ,Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer

from server.servers import server_renew_and_start_tcp_and_tun
from lib.serversApi import ServersApi
from modal import UserBuyProductModal, UserModal
from lib.db import get_database
from lib.deps import get_current_user
from server.product import get_product_by_id,update_user_balance

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def serialize_mongo_document(document):
    # Convert ObjectId to string and serialize the document
    return {k: str(v) if isinstance(v, ObjectId) else v for k, v in document.items()}

@router.get("/list", summary="获取商品列表")
async def get_product_list(current_user: UserModal = Depends(get_current_user)):
  try:
    database = await get_database()
    productList = database.product.find({}, {'product_id': 0}).sort("price", 1)
    return {"msg": "success","data":[serialize_mongo_document(product) async for product in productList]}
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="获取商品列表失败")

@router.post("/buy",summary="产品购买")
async def buy(backgroundTasks: BackgroundTasks,item: UserBuyProductModal,current_user: UserModal = Depends(get_current_user)):
  
  product = await get_product_by_id(item.id)
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="产品不存在")
    
  price = int(product["price"]) * item.month
  if current_user["balance"] < price:
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="余额不足")
    

  # 调用购买接口
  serverApi = ServersApi()
  server_id = serverApi.buy(product["product_id"],item.month)
  if not server_id:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="服务器创建失败，请稍后再试")
  # 通过脚本实时匹配数据库中购买完成未分配信息的资源
  
  '''
  后台任务
    1. 创建成功后,开启虚拟化,开启TUN/TAP
    2. 如果购买的月份大于一个月，调用续费接口
  '''
  backgroundTasks.add_task(server_renew_and_start_tcp_and_tun, item.month > 1 , server_id,item.month - 1)
  # 购买结束
  
  await update_user_balance(current_user["id"], price) # 扣款
  
  database = await get_database()
  database.servers.insert_one({
    "userId": ObjectId(current_user["id"]),
    "productId": ObjectId(item.id),
    "id": server_id,
    "createAt": int(time.time() * 1000),
    "endAt": int(time.time() * 1000) + 3600 * 24 * 30 * item.month,
    "month": item.month
    }
  )
  return {
    "status": "success",
    "msg": "购买成功！",
    "data": {
        "id": server_id
      }
  }
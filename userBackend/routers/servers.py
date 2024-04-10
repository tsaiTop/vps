from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from modal import ServerSetStatusModal, UserModal
from server.servers import query_database, query_user_servers_list_byId
from routers.product import serialize_mongo_document
from lib.deps import get_current_user
from lib.serversApi import ServersApi

router = APIRouter()

@router.get("/list",summary="获取服务器列表")
async def get_servers_list(current_user: UserModal = Depends(get_current_user)):
  try:
    results = await query_user_servers_list_byId(current_user["id"])
    return {"msg": "success", "data": [serialize_mongo_document(i) for i in results]}
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
  
@router.get("/os/list",summary="获取操作系统列表")
async def get_os_list(server_id: str, current_user: UserModal = Depends(get_current_user)):
  isQuery = await query_database({"id": server_id, "userId": ObjectId(current_user["id"])})
  if not isQuery:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有找到该服务器！")
  
  serverApi = ServersApi()
  osList =  serverApi.getServerOsById(server_id)
  return {
    "status": "success",
    "msg": "获取成功！",
    "data": osList
  }
  
@router.post("/reinstall",summary="重装系统")
async def reinstall(server_id: str, os_id: str, current_user: UserModal = Depends(get_current_user)):
 
  isQuery = await query_database({"id": server_id, "userId": ObjectId(current_user["id"])})
  if not isQuery:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有找到该服务器！")
    
  serverApi = ServersApi()    
  isReInstall = serverApi.serverReinstall(server_id, os_id)
  if isReInstall["status"] != "success":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=isReInstall["msg"])
    
  return {
    "status": "success",
    "msg": "重装成功！"
  }
  
@router.post("/status",summary="更改服务器状态")
async def server_set_status(item: ServerSetStatusModal):
  server_id, status, current_user = item.server_id, item.status, item.current_user
    
  isQuery = await query_database({"id": server_id, "userId": ObjectId(current_user["id"])})
  if not isQuery:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有找到该服务器！")
    
  serverApi = ServersApi()
  result = serverApi.serverSetStatus(server_id, status)
  if result["status"] != "success":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["msg"])
    
  return {
      "status": "success",
      "msg": f"{status}成功！",
  }

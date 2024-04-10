from bson.objectid import ObjectId
from lib.serversApi import ServersApi
from lib.db import get_database


async def query_user_servers_list_byId(userId):
  database = await get_database()
  database = await get_database()
  pipeline = [
        {
            "$match": {
                "userId": ObjectId(userId)
            }
        },
        {
            "$lookup": {
                "from": "product",
                "localField": "productId",
                "foreignField": "_id",
                "as": "productInfo"
            }
        },
        {
            "$unwind": "$productInfo"  # 展开productInfo数组
        },
        {
            "$project": {
                "userId": 0, 
                "productId": 0,
                "productInfo.userId": 0 ,
                "productInfo.product_id": 0,
                "productInfo._id": 0
            }
        }
    ]

  results = database.servers.aggregate(pipeline)
  return results

# 查询数据库
async def query_database(query: dict, projection: dict = None):
    database = await get_database()
    return database.servers.find_one(query, projection)


# 启用续费,开启TCP,虚拟化
async def server_renew_and_start_tcp_and_tun(isTrue: bool, server_id: str, month: int):
    serverApi = ServersApi()
    if isTrue:
        serverApi.serverRenew(server_id, month - 1)
    # 开启虚拟化和开启TUN/TAP 接口暂无实现
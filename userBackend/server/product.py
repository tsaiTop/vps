from bson.objectid import ObjectId

from lib.db import get_database

async def get_product_by_id(product_id: str):
  database = await get_database()
  return database.product.find_one({"_id": ObjectId(product_id)})
  
async def update_user_balance(user_id: str, amount: int):
  database = await get_database()
  return database.users.update_one({"_id": ObjectId(user_id)}, {"$inc": {"balance": -amount}})
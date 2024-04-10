from db.database import connect_mongodb

async def get_database():
  _, database = await connect_mongodb()
  return database
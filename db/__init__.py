from motor.motor_asyncio import AsyncIOMotorClient

from config import DB_URI, DB_NAME

client = AsyncIOMotorClient(DB_URI)
database = client[DB_NAME]
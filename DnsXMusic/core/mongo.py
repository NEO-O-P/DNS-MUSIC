from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client
import asyncio
import config
from ..logging import LOGGER

# Hardcoded fallback database (Security Tip: Apna khud ka use karein)
TEMP_MONGODB = "mongodb+srv://kuldiprathod2003:kuldiprathod2003@cluster0.wxqpikp.mongodb.net/?retryWrites=true&w=majority"

# Logger fix
logger = LOGGER(__name__)

if config.MONGO_DB_URI is None:
    logger.warning(
        "𝐍o 𝐌ONGO 𝐃B 𝐔RL 𝐅ound.. 𝐘our 𝐁ot 𝐖ill 𝐖ork 𝐎n 𝐕𝐈𝐏 𝐌𝐔𝐒𝐈𝐂 𝐃atabase"
    )
    
    # Temporary client setup to get bot username
    temp_client = Client(
        "TempManager",
        bot_token=config.BOT_TOKEN,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        in_memory=True,
    )
    
    try:
        # Client start karke username nikalna
        temp_client.start()
        info = temp_client.get_me()
        db_name = info.username
        temp_client.stop()
    except Exception as e:
        logger.error(f"Failed to fetch bot username for DB: {e}")
        db_name = "DNS_Music_Bot" # Fallback name agar username na mile

    _mongo_async_ = _mongo_client_(TEMP_MONGODB)
    _mongo_sync_ = MongoClient(TEMP_MONGODB)
    mongodb = _mongo_async_[db_name]
    pymongodb = _mongo_sync_[db_name]
else:
    # Agar user ne apni URI di hai
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    mongodb = _mongo_async_.DnsMusic # Database name consistent rakha hai
    pymongodb = _mongo_sync_.DnsMusic

logger.info("MongoDB Connection Established.")

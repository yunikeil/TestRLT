import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from core.settings import config

# Я в основном работал с SQLAlchemy и PostgreSQL, потому у меня нет опыта в организации работы с Mongo
# Из-за этого могут быть проблемы с сессиями и поддержкой проекта при высокой нагрузке

__logger = logging.getLogger("telegram")

mongo_client = AsyncIOMotorClient(
    config.MONGO_URL, server_api=ServerApi('1'), timeoutms=5000,
)


async def ping_mongo_server(*, mongo_client: AsyncIOMotorClient = mongo_client):
    """Проверяем есть ли соединение с MongoDB сервером

    :param mongo_client: Объект клиента для работы с MongoDB, defaults to mongo_client
    :type mongo_client: AsyncIOMotorClient, optional
    """
    await mongo_client.admin.command('ping')
    __logger.info("Ping to MongoDB completed!")

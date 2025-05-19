from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Асинхронная строка подключения (использует asyncpg)
ASYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=True,  # Логирование SQL-запросов (только для разработки)
    pool_pre_ping=True  # Проверка соединения перед использованием
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
from app.db.base import Base
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

target_metadata = Base.metadata

def run_migrations_online():
    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        
        with context.begin_transaction():
            context.run_migrations()
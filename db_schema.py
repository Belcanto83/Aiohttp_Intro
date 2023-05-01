import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()
DSN = f'postgresql+asyncpg://{os.getenv("PG_USER")}:{os.getenv("PG_PASSWORD")}@' \
      f'{os.getenv("PG_HOST")}:{os.getenv("PG_PORT")}/{os.getenv("PG_DB")}'
engine = create_async_engine(DSN)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///whitelist.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass


class User(Base):
    """Модель пользователя для хранения ID пользователей в белом списке.

       Attributes:
           id (int): Уникальный идентификатор пользователя.
           telegram_id (int): ID пользователя в Telegram.
       """
    __tablename__ = 'whitelist'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)

def init_db():
    """Создает все таблицы в базе данных на основе определенных моделей."""
    Base.metadata.create_all(bind=engine)

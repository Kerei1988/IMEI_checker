from sqlalchemy.orm import Session
from db.database import User


def add_user_to_whitelist(db: Session, telegram_id: int):
    """Добавляет пользователя в белый список.
        Args:
            db (Session): Сессия базы данных.
            telegram_id (int): ID пользователя в Telegram.
        Returns:
            User: Добавленный пользователь.
        """
    user = User(telegram_id=telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def is_user_in_whitelist(db: Session, telegram_id: int) -> bool:
    """Проверяет, находится ли пользователь в белом списке.
        Args:
            db (Session): Сессия базы данных.
            telegram_id (int): ID пользователя в Telegram.
        Returns:
            bool: True если пользователь в белом списке, иначе False.
        """
    return db.query(User).filter(User.telegram_id == telegram_id).first() is not None

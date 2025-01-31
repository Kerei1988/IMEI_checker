
from pydantic import BaseModel, Field


class CheckIMEI(BaseModel):
    """Модель для проверки IMEI.
       Этот класс используется для валидации входящих данных при запросе на проверку IMEI.
       Attributes:
           imei (str): IMEI устройства, который должен быть длиной от 15 до 16 символов.
           Token (str): Токен API для авторизации запроса.
       """
    imei: str = Field(min_length=15, max_length=16)
    token: str

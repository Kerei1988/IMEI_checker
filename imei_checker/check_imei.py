import requests


def check_imei(imei, token_api):
    """Проверяет IMEI устройства с использованием API IMEI Check.
       Отправляет запрос на проверку IMEI и возвращает ответ от API.
       Args:
           imei (str): IMEI устройства для проверки. Должен быть длиной 15 или 16 цифр.
           token_api (str): Токен API для авторизации запроса.
       Returns:
           dict: Ответ от API в формате JSON, содержащий информацию об устройстве.
                 Если произошла ошибка, возвращается None.
       Raises:
           Exception: Если запрос к API завершился неудачно, будет выведено сообщение об ошибке.
       """
    url = "https://api.imeicheck.net/v1/checks"
    headers = {'Authorization': f'Bearer {token_api}',
               'Accept-Language': 'ru',
               'Content-Type': 'application/json'
               }
    payload = {
        "deviceId": f"{imei}",
        "serviceId": 12,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f'Ошибка: {str(e)}')
        return None

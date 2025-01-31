import os
from dotenv import load_dotenv

from telebot import TeleBot, types

from imei_checker.check_imei import check_imei
from db.database import SessionLocal, init_db
from db.func_database import is_user_in_whitelist, add_user_to_whitelist

load_dotenv(".env.py")


bot = TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
token_api =os.getenv('API_TOKEN')

init_db()

@bot.message_handler(func= lambda message: True)
def handle_message(message):
    """Обрабатывает входящие сообщения от пользователей.
    Проверяет наличие пользователя в белом списке и отвечает на команды.
    Args:
        message (Message): Сообщение от пользователя.
    """
    db = SessionLocal()

    if not is_user_in_whitelist(db, message.from_user.id):
        bot.reply_to(message, 'У вас нет доступа!')
        add_user_to_whitelist(db, message.from_user.id)
        return None
    if message.text.startswith("/start"):
        markup = types.ReplyKeyboardMarkup()
        button_imei = types.KeyboardButton('Проверка IMEI')
        markup.add(button_imei)
        bot.send_message(message.chat.id, "Привет! Я могу проверить IMEI устройство.", reply_markup=markup)
    elif message.text == "Проверка IMEI":
        msg = bot.send_message(message.chat.id, "Введите IMEI для проверки.")
        bot.register_next_step_handler(msg, process_imei)


def process_imei(message):
    """Обрабатывает ввод IMEI от пользователя.
      Проверяет длину IMEI и отправляет запрос на проверку.
      Args:
          message (Message): Сообщение от пользователя с введенным IMEI.
      """
    msg = message.text.strip()
    if len(msg) not in [15, 16]:
        print("IMEI не верный (Длина 15 -16 цифр)")
    else:
        response = check_imei(msg, token_api=token_api)
        response = format_imei_response(response)
        if response is None:
            bot.reply_to(message, "Ошибка при проверке IMEI. Попробуйте позже.")
        else:
            bot.reply_to(message, f"Информация об IMEI:\n{response}")


def format_imei_response(response):
    """Форматирует ответ от API проверки IMEI в удобочитаемый текст.
        Извлекает информацию из ответа API и формирует строку с данными об устройстве.
        Args:
            response (dict): Ответ от API, содержащий информацию об IMEI устройства.
                             Ожидается, что ответ включает ключи 'id', 'status', 'service',
                             'properties' и другие.
        Returns:
            str: Форматированная строка с информацией об устройстве, включая ID, статус,
                 имя устройства, IMEI, MEID, серийный номер и статус гарантии.
                 Если изображение доступно, оно также будет включено в строку.
        """
    properties = response.get('properties', {})
    formatted_text = (
        f"ID: {response.get('id', 'Не указано')}\n"
        f"Статус: {response.get('status', 'Не указано')}\n"
        f"Сервис: {response.get('service', {}).get('title', 'Не указано')} (ID: {response.get('service', {}).get('id', 'Не указано')})\n"
        f"Имя устройства: {properties.get('deviceName', 'Не указано')}\n"
        f"IMEI: {properties.get('imei', 'Не указано')}\n"
        f"MEID: {properties.get('meid', 'Не указано')}\n"
        f"Серийный номер: {properties.get('serial', 'Не указано')}\n"
        f"Статус гарантии: {properties.get('warrantyStatus', 'Не указано')}\n"
        f"В черном списке GSMA: {'Да' if properties.get('gsmaBlacklisted') else 'Нет'}\n"
    )

    image_url = properties.get('image')
    if image_url:
        formatted_text += f"\nИзображение устройства:\n{image_url}"

    return formatted_text.strip()


if __name__ == "__main__":
    bot.polling(none_stop=True)
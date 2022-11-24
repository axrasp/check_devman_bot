import logging
import textwrap as tw
import time

import requests
from environs import Env
from requests.exceptions import ConnectionError, ReadTimeout
from telegram import Bot

logger = logging.getLogger('Logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_notification(bot, tg_chat_id, message):
    chat_id = tg_chat_id
    for attempts in message['new_attempts']:
        if attempts['is_negative']:
            text = f'''\
                    -------------------
                    Задание проверено:
                    *"{attempts['lesson_title']}"*.
                    \
                    😔😔😔
                    К сожалению в нем есть недочеты, подробнее по ссылке:
                    \
                    {attempts['lesson_url']}
                    \
                    '''
        else:
            text = f'''\
                    -------------------
                    Задание проверено:
                    *"{attempts['lesson_title']}"*.
                    \
                    😎😎😎
                    Ура! Можно двигаться дальше! Подробнее:
                    \
                    {attempts['lesson_url']}
                    '''
        bot.send_message(chat_id=chat_id,
                         text=tw.dedent(text),
                         parse_mode='Markdown'
                         )


def main():
    env = Env()
    env.read_env()
    bot_token = env.str('BOT_TOKEN')
    bot = Bot(bot_token)
    tg_chat_id = env.str('TG_CHAT_ID')
    devman_token = env.str('DEVMAN_TOKEN')
    timestamp = ''
    url = "https://dvmn.org/api/long_polling/"

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(tg_bot=bot, chat_id=tg_chat_id))

    headers = {
        'Authorization': f'Token {devman_token}'
    }
    while True:
        try:
            logger.warning('Бот запущен')
            while True:
                payload = {
                    'timestamp': timestamp
                }
                try:
                    response = requests.get(
                        url,
                        params=payload,
                        headers=headers,
                        timeout=100
                    )
                    response.raise_for_status()
                    review_status = response.json()
                    if review_status['status'] == 'found':
                        send_notification(bot=bot,
                                          tg_chat_id=tg_chat_id,
                                          message=review_status
                                          )
                        timestamp = review_status['last_attempt_timestamp']
                        continue

                    timestamp = review_status['timestamp_to_request']

                except ReadTimeout:
                    continue

                except ConnectionError:
                    logger.error('Потеряно соединение')
                    time.sleep(5)
                    logger.warning('Перезапуск бота')
                    continue

        except Exception as e:
            logger.error('Бот упал с ошибкой:')
            logger.error(e, exc_info=True)
            logger.warning('Перезапуск бота')
            continue


if __name__ == "__main__":
    main()

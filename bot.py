import textwrap as tw
import time

import requests
from environs import Env
from requests.exceptions import ConnectionError, ReadTimeout
from telegram import Bot


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

    while True:
        headers = {
            'Authorization': f'Token {devman_token}'
        }
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
        except ConnectionError as e:
            print(e)
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()

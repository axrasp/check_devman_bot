import pprint
import time

import requests
from environs import Env
from requests.exceptions import ConnectionError, ReadTimeout
from telegram import Bot


def send_notification(bot, message):
    chat_id = bot.get_updates()[-1].message.chat_id
    for attempts in message['new_attempts']:
        if attempts['is_negative']:
            text = f'''
-------------------
Задание проверено:
*"{attempts['lesson_title']}"*.

😔😔😔
К сожалению в нем есть недочеты, подробнее по ссылке:

{attempts['lesson_url']}

'''
        else:
            text = f'''
-------------------
Задание проверено:
*"{attempts['lesson_title']}"*.

😎😎😎
Ура! Можно двигаться дальше! Подробнее:

{attempts['lesson_url']}

'''
        bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')


def main():
    env = Env()
    env.read_env()
    bot_token = env.str('BOT_TOKEN')
    bot = Bot(bot_token)
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
            if response.json()['status'] == 'found':
                send_notification(bot=bot, message=response.json())
                continue
            pprint.pprint(response.json())
            timestamp = response.json()['timestamp_to_request']
        except ReadTimeout as e:
            print(e)
            continue
        except ConnectionError as e:
            print(e)
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()

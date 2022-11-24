# Бот для уведомления о проверке задания в школе DEVMAN

Позволяет получать уведомоления в Telegram, когда задача проверена преподователем

## Установка

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Получение чувствительных данных

Создайте бота в телеграме через [https://t.me/BotFather](https://t.me/BotFather)

Создайте файл ``.env`` и добавьте в него следующие данные вида:

```
DEVMAN_TOKEN="23422424244224442"
BOT_TOKEN="57322135551:AAEUFDZDBE"
```

- DEVMAN_TOKEN - токен в вашем личном кабинете [школы Devman](https://dvmn.org/api/docs/) 
- BOT TOKEN - токен от телеграм бота
- TG_CHAT_ID - ваш номер chat_id, его можно получить в [боте](https://t.me/getmyid_bot)

## Запуск на локальном сервере

Запустите бот командой:

```
python3 bot.py
```

Запусите бота в телегамме ``/start``


## Деплой на сервер Heroku

Репозиторий готов к деплою на сервер Heroku, [подробная инструкция](https://teletype.in/@cozy_codespace/Hk70-Ntl4?ysclid=l8fv8rmn9x968256359)

## Деплой на свой сервер

Загрузите репозиторий на сервер (в этом примере грузим в /opt/your_bot_name).
Создайте виртуальное окружение в папке бота:

```commandline
python3 -m venv venv
```

Активируйте виртуальное окружение:

```
source venv/bin/activate
```
Установите зависимости и чувствительные данные (см. раздел Установка)

### Демонизация бота

Создайте новый файл в папке ``/etc/systemd/system`` с названием ``your_bot_name.service`` c таким содержимым:

```
[Service]
ExecStart=/opt/your_bot_name/venv/bin/python3 /opt/your_bot_name/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Добавляем бота в автозагрузку

```commandline
systemctl enable your_bot_name
```

Запускаем бота:

```commandline
systemctl start your_bot_name
```

Подробнее о systemd [здесь](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
Туториал [здесь](https://4te.me/post/systemd-unit-ubuntu/)
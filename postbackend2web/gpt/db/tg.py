from aiogram import Bot, Dispatcher, executor, types
import asyncio
import sqlite3
import time
import aiosqlite
import os

API_TOKEN = '6736255737:AAGosoGQ-qewdByjVV20yf-pv2uFhcr7QuU'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_ids = set()  # Список ID пользователей
  # Список для хранения API ключей

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids.add(user_id)

        await message.answer("Вы успешно подписались на рассылку.")
    else:
        await message.answer("Вы уже подписаны.")
@dp.message_handler(commands=['msg'])
async def broadcast_message(message: types.Message):
    if message.from_user.id in user_ids:  # Проверка на разрешенного пользователя
        await send_message_to_users("API Warning")
    else:
        await message.reply("У вас нет прав использовать эту команду.")
async def send_message_to_users(message_text):
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


async def check_db():
    old_length = 0
    while True:
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute("SELECT * FROM logs")

        rows=c.fetchall()

        lenth = len(rows)
        conn.close()


        if lenth > old_length:

            print("New data found!",rows[-1])
            # Здесь вы можете отправить сообщение в Telegram, если найдено новое данные
            old_length=lenth
        await asyncio.sleep(30)  # Проверяем каждую секунду

# Обработчик команды /API
@dp.message_handler(commands=['API'])
async def api_command(message: types.Message):
    await message.answer("Жду файл с API ключами.")

# Обработчик для получения документа
@dp.message_handler(content_types=['document'])
async def handle_docs(message: types.Message):
    api_keys = []
    proxies = []
    document_id = message.document.file_id
    file = await bot.get_file(document_id)
    file_path = file.file_path
    contents = await bot.download_file(file_path)
    caption = message.caption

    # Чтение и обработка файла
    text =  contents.getvalue().decode('utf-8')
    keys = text.split('\n')
    if caption=='API':
        for key in keys:
            if key.strip():  # Проверка на пустые строки
                api_keys.append(key)

                conn = sqlite3.connect('db.db')
                c = conn.cursor()
                c.execute("""
                    INSERT INTO keys (key, state, timestamp) VALUES (?, ?,?)
                """, (key, "1", time.time()))
                conn.commit()

        print(api_keys)
        await message.answer("API ключи получены и сохранены.")
    elif caption=='PROXY':
        for proxy in keys:
            if proxy.strip():  # Проверка на пустые строки
                proxies.append(proxy)
                link,host,log,pas=proxy.split(':')
                print(proxy)
                conn = sqlite3.connect('db.db')
                c = conn.cursor()
                c.execute("""
                    INSERT INTO proxy (type, state, link, auth) VALUES (?, ?,?,?)
                """, ("socks5", "1",link+":"+host,log+":"+pas))
                conn.commit()

        print(proxies)
        await message.answer("proxy получены и сохранены.")
# Остальные обработчики...

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_db())
    executor.start_polling(dp, skip_updates=True)
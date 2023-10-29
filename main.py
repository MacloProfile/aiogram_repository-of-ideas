import logging
from aiogram import Bot, Dispatcher, types
import psycopg2

API_TOKEN = 'TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
conn = psycopg2.connect(dbname='Ideas', user='postgres', password='postgres')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для сохранения сообщений. "
                         "Используй команду /save \"текст\", чтобы сохранить своё сообщение в базе данных.")

@dp.message_handler(commands=['save'])
async def cmd_save(message: types.Message):
    try:
        message_text = message.get_args()[2:]
        user_id = message.from_user.id

        print(message_text)

        # add text to BD
        cur = conn.cursor()
        cur.execute("INSERT INTO savedMessages (user_id, message_text) VALUES (%s, %s)", (user_id, message_text))
        conn.commit()
        cur.close()

        await message.answer(f"Твоё сообщение успешно сохранено в базе данных!")

    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении сообщения: {e}")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

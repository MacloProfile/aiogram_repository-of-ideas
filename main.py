import logging
from aiogram import Bot, Dispatcher, types
import psycopg2

API_TOKEN = '6599440063:AAFT5XN8VFowLyDsU4H9tIPYhX0v0P4KSUQ'

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
        message_text = message.get_args()
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


@dp.message_handler(commands=['get'])
async def cmd_get(message: types.Message):
    try:
        id = message.get_args()

        cur = conn.cursor()
        cur.execute("SELECT message_text FROM savedMessages WHERE id = %s", (id,))
        result = cur.fetchone()
        cur.close()

        if result:
            await message.answer(f"Ваше сообщение (ID {id}):\n{result[0]}")
        else:
            await message.answer("Сообщение с указанным ID не найдено.")

    except Exception as e:
        await message.answer(f"Произошла ошибка при получении сообщения: {e}")

def create_table():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS savedMessages (
            id serial PRIMARY KEY,
            user_id BIGINT NOT NULL,
            message_text text NOT NULL
        )
    """)
    conn.commit()
    cur.close()


if __name__ == '__main__':
    create_table()
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests

API_TOKEN = '6937115273:AAHKEuhoYriJmW4UqEISc7plPijwRxrSbGs'


# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Словарь для хранения заявок
bookings = {}

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    print(message)
    await message.reply('Привет, я бот для бронирования столиков заведений города могилёва.\n'
                        'В будущем количество городов может увеличиваться')
    await message.reply('/Mogilev')


    @dp.message_handler(commands=['Mogilev'])
    async def mogilev_handler(messages: types.Message):
        await message.reply(f'Вы выбрали город /Mogilev,\n'
                            f'вам доступны:\n'
                            f'/Bar,\n'
                            f'/Restorant,\n'
                            f'/Kafe')


        @dp.message_handler(commands=['Bar'])
        async def mogilev_handler(messages: types.Message):
            await message.reply(f'Вы выбрали /Bar,\n'
                                f'Вот все бары города могилёва: \n'
                                f'/Mint - Мята\n'
                                f'/MONARCH\n')


            @dp.message_handler(commands=['Mint'])
            async def mint_handler(messages:types.Message):
                await message.reply('https://mogilev.myataofficial.com')
                await message.reply('Вы хотите забронировать тут место?\n'
                                    '/yes\n'
                                    '/no')


                @dp.message_handler(commands=['yes'])
                async def book_table(message: types.Message):
                    user_id = message.from_user.id
                    if user_id not in bookings:
                        bookings[user_id] = {}
                    bookings[user_id]['status'] = 'pending'
                    await message.reply("Для бронирования столика, пожалуйста, укажите дату и время.")



# Команда для администратора для просмотра и подтверждения заявок
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id == 5207148273:
        admin_message = "Список заявок:\n"
        for user_id, booking_info in bookings.items():
            if booking_info['status'] == 'pending':
                admin_message += f"Пользователь {user_id} хочет забронировать столик.\n"
        if admin_message == "Список заявок:\n":
            admin_message = "Заявок на бронирование столиков нет."
        await message.reply(admin_message)

# Обработчик сообщений для ввода даты и времени бронирования
@dp.message_handler(lambda message: bookings.get(message.from_user.id) and bookings[message.from_user.id]['status'] == 'pending')
async def process_booking_date_time(message: types.Message):
    user_id = message.from_user.id
    if user_id in bookings:
        bookings[user_id]['date_time'] = message.text
        bookings[user_id]['status'] = 'submitted'
        await message.reply(f"Вы забронировали столик на {message.text}. Администратор рассмотрит вашу заявку.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
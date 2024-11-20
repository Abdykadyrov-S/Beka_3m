from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Автозапчасти', callback_data='auto'), InlineKeyboardButton(text='Мобильные запчасти', callback_data='mobile')]
])

confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подвердить', callback_data='confirm')]
])

"Автозапчасти"
categories = {
        'Воздущный фильтр': 1200,
        'Тормозные колодки': 1500,
        'Аккумулятор': 5000,
}
"Мобильные запчасти"
categories2 = {
        'Экран для Iphone 13': 6000,
        'Зарядное устройство': 1000,
        'Сенсорная панель для Samsung': 2000,
    }

orders = {}

@dp.message(Command("start"))
async def start(message:types.Message):
    await message.answer("Вас приветсвует магазин автозапчастей и мобильных запчастей \nВыберите категорию: /menu")

@dp.message(Command("menu"))
async def menu_command(message:types.Message):
    await message.answer("Категории:", reply_markup=menu_keyboard)

@dp.callback_query(F.data == 'auto')
async def menu_command(callback:types.CallbackQuery):
    # await message.answer("Категории:")
    builder = InlineKeyboardBuilder()
    for zapchast, price in categories.items():
        builder.button(
            text=f"{zapchast} - {price}",
            callback_data=f'menu_{zapchast}'
        )
    builder.adjust(2)
    await callback.message.edit_text("Категории: ", reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'mobile')
async def menu_command(callback:types.CallbackQuery):
    # await message.answer("Категории:")
    builder = InlineKeyboardBuilder()
    for zapchast, price in categories2.items():
        builder.button(
            text=f"{zapchast} - {price}",
            callback_data='zapchast'
        )
    builder.adjust(2)
    await callback.message.edit_text("Категории: ", reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'zapchast')
async def menu_command(callback:types.CallbackQuery):
    await callback.message.edit_text('Подвердите заказ', reply_markup=confirm_keyboard)

@dp.callback_query(F.data == 'confirm')
async def menu_command(callback:types.CallbackQuery):
    await callback.message.edit_text('Спасибо за покупку')

# @dp.message(Command("menu"))
# async def menu_command(message:types.Message):
#     builder = InlineKeyboardBuilder()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

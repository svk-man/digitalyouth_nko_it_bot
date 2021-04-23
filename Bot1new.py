from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import database
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token = '1756077502:AAEW_cavIZErG8g6pCK_axKOafPtxNB--8s')
dp = Dispatcher(bot)

class reg(StatesGroup):
    # для it
    name = State()
    field = State()
    # для НКО
    title = State()
    # для модераторов
    key = State()
    # общие
    ready = State()

@dp.message_handler (commands = ['help'])
async def process_start_command(message: types.Message):
    await message.reply('Здесь выводится информация о боте и подсказки')


#попытка сделать кнопку регистрации
but_reg = KeyboardButton('/регистрация')
regis = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True).add(but_reg)

@dp.message_handler(commands = ['start'])
async def new_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет!  \nТы ещё не зарегистрирован, прошу пройти небольшую регистрацию :)',
                           reply_markup = regis)
    
#Кнопки

inline_btn_1 = InlineKeyboardButton('Кнопка №1', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)


#Это пул кнопок
inline_but_pool = InlineKeyboardMarkup()

inline_bt1 = InlineKeyboardButton('Представитель IT', callback_data='btn1')
inline_bt2 = InlineKeyboardButton('Представитель НКО', callback_data='btn2')
inline_bt3 = InlineKeyboardButton('Модератор', callback_data='btn3')
inline_but_pool.add(inline_bt1, inline_bt2, inline_bt3)

@dp.message_handler(commands = ['регистрация'])
async def proc_com(message: types.Message):
    await message.reply('В качестве кого Вы хотите зарегистрироваться?', reply_markup = inline_but_pool)

    
#Попытка сделать развилку как планировали
@dp.callback_query_handler(lambda c1: c1.data and c1.data.startswith('btn'))
async def call_but_pool(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]    
    if code.isdigit():
        code = int(code)
    if code == 1:        
        await bot.send_message(callback_query.from_user.id, 'Введите ваше Имя')
        await reg.name.set() # меняем статус на ожидание имени
    if code == 2:
        await bot.send_message(callback_query.from_user.id, 'Введите наименование НКО')
        await reg.title.set()
    if code == 3:
        await bot.send_message(callback_query.from_user.id, 'Введите Ваш ключ для регистрации')
        await reg.key.set()
        
# сценарий для it после введения имени
@dp.message_handler(state=reg.name) # запускается при значении статуса "name"
async def process_message(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id) # фиксируем id
    await state.update_data(name=message.text) # фиксируем имя
    await bot.send_message(message.from_user.id, 'Введите сферу своей деятельности')
    await reg.field.set() # меняем статус на сферу деятельности

@dp.message_handler(state=reg.field) # запускается при статусе сфера деятельности
async def process_message(message: types.Message, state: FSMContext):
    await reg.ready.set() # меняем статус - данные собраны
    await state.update_data(field=message.text) # фиксируем значения сферы деятельности
    user_data = await state.get_data() # получаем словарь с данными пользователя
    data = tuple(user_data.values()) # представляем в виде кортежа для занесения в бд
    with connection.cursor() as cursor: # заносим в бд
        cursor.executemany(insert_it_query, data)
        connection.commit()

# сценарий для НКО после введения названия
@dp.message_handler(state=reg.title)
async def process_message(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    await state.update_data(title=message.text)
    await reg.ready.set()
    user_data = await state.get_data()
    data = tuple(user_data.values())
    with connection.cursor() as cursor:
        cursor.executemany(insert_nko_query,
                           data)
        connection.commit()

# сценарий для НКО после введения названия
@dp.message_handler(state=reg.key)
async def process_message(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    await state.update_data(key=message.text)
    await reg.ready.set()
    user_data = await state.get_data()
    data = tuple(user_data.values())
    with connection.cursor() as cursor:
        cursor.executemany(insert_moderator_query,
                           data)
        connection.commit()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
    

from config import TOKEN, ADMIN_ID
import logging
from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from db import create_table, save_photo, get_photo, exist_photo

class Form(StatesGroup):
  add = State()

create_table()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

kb = types.InlineKeyboardMarkup()
kb.add(
  types.InlineKeyboardButton(text='Футболки', callback_data='tshorts')
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  await message.reply('Привет, выбери товар', reply_markup=kb)

akb = types.InlineKeyboardMarkup()
akb.add(types.InlineKeyboardButton(text='MaisonMargiela', callback_data='mm6'))

@dp.callback_query_handler(lambda call: call.data == 'tshirts')
async def tshirts(call: types.CallbackQuery):
  await call.answer()
  await call.message.edit_text('Выберите футболку', reply_markup=akb)

@dp.callback_query_handler(lambda call: call.data == 'mm6')
async def mm6(call: types.CallbackQuery):
  await call.answer()
  check = types.InlineKeyboardMarkup()
  check.add(types.InlineKeyboardButton(text='Посмотреть фото', callback_data='mm6_check'))
  await call.message.edit_text("Стоимость футболки - 7000тг",reply_markup=check)

@dp.callback_query_handler(lambda call: call.data == 'mm6_check')
async def mm6_check(call: types.CallbackQuery):
  mm6 = get_photo()
  if mm6:
    file_id = mm6[-1][0]
    check = exist_photo(file_id)

    if check is None:
      await call.message.answer('Фото пока не добавлено, но оно скоро добавится!')
    else:
      await bot.send_photo(call.message.chat.id, file_id)
  else:
    await call.message.answer('Фото пока не добавлено, но оно скоро добавится!')


admin_kb = types.InlineKeyboardMarkup()
admin_kb.add(types.InlineKeyboardButton(text='Добавить фото к товару', callback_data='add_photo'))

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
  if message.from_user.id == ADMIN_ID:
    await message.reply('Это админский раздел', reply_markup=admin_kb)
  else:
    await message.answer("У вас нет доступа к этому разделу")
    return


@dp.callback_query_handler(lambda call: call.data == 'add_photo')
async def photo_request(call: types.CallbackQuery):
  await call.answer()
  await call.message.answer('Отправь фото')
  await Form.add.set()
  

@dp.message_handler(content_types=['photo'], state=Form.add)
async def add_photo(message: types.Message, state: FSMContext):
  tshirt = message.photo[-1].file_id
  save_photo(tshirt)
  await message.answer('Фото добавлено')
  await state.finish()
  


  
korz = types.InlineKeyboardMarkup()
korz.add(
  types.InlineKeyboardButton(text='MeisonMargiela', callback_data='mm6')
)

@dp.callback_query_handler(lambda call: call.data == 'tshorts')
async def mm6(call: types.CallbackQuery):
  await call.message.answer('Выберите товар: ', reply_markup=korz)


  





if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
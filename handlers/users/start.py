import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import logging
from data.config import ADMINS
from filters.admin import AdminFilter
from loader import dp, db, bot
from states.test_states import AnswerState, AnswersState, TestState
from keyboards.inline.results import answer
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!, nimadir botga xush kelibsiz!")
    try:
        db.add_user(user_id=message.from_user.id)
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=message.from_user.id, text="Siz ro'yxatdan o'tgansiz!")



@dp.message_handler(commands="send_test", state=None)
async def bot_send_test(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Test raqami va savollarini yuboring: ")
        await TestState.questions.set()
    else:
        
        print(ADMINS, message.from_user.id)
        await message.answer("Siz test yubora olmaysiz!")
    
@dp.message_handler(state=TestState.questions)
async def test_state_handler(message: types.Message, state: FSMContext):
    test = message.text
    users = db.select_all_users()
    for user_id in users:
        try:
            await bot.send_message(user_id[0], text=test, reply_markup=answer)
            await message.answer("Test yuborildi")
            await state.finish()
        except Exception as e:
            logging.exception(f"Xatolik sodir bo'ldi: {e}")
    
        
            
@dp.callback_query_handler(text="send_answers", state=None)
async def test_send_answers(call: types.CallbackQuery):
    await call.message.answer("Test raqamini kiriting: ")
    db.create_table_answers()
    await AnswerState.number.set()
    
@dp.message_handler(state=AnswerState.number)
async def answer_number_state(message: types.Message, state: FSMContext):
    try:
        number = int(message.text)
        await state.update_data(
            {'number': number}
        )
        await message.answer("Barcha javoblarni bitta habarning o'zida yuboring: ")
        await AnswerState.answer.set()
    except ValueError as e:
        print("Raqam xato kiritildi. Test raqamini to'g'ri kiriting: ")
    
    
@dp.message_handler(state=AnswerState.answer)
async def answer_answer_state(message: types.Message, state: FSMContext):
    print(message.text)
    try:
        answer = message.text
        data = await state.get_data()
        number = data.get('number')
        print(answer, number)
        db.add_answer(
            user_id=message.from_user.id, 
            user_name=message.from_user.full_name,
            username = message.from_user.username,
            answer_number=number, 
            answer=answer
        )
        await message.reply("Javobingiz yuborildi ✅\nTez orada natijalarni e'lon qilamiz! ⏳")
        await state.finish()
    except Exception as e:
        print(e)
        await message.reply("Javoblar xato yuborildi. Qaytadan yuboring: ")
        
        
        
@dp.message_handler(commands="all_answers", state=None)
async def get_all_answers(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Qaysi test natijalarini ko'rmoqchisiz?\nTest raqamini kiriting: ",)
        await AnswersState.number.set()
    else:
        
        print(ADMINS, message.from_user.id)
        await message.answer("Siz test natijalarini ko'ra olmaysiz!")
        
@dp.message_handler(state=AnswersState.number)
async def get_answers_state(message: types.Message, state: FSMContext):
    try:
        number = int(message.text)
        answers = db.select_all_answers(number)
        for answer in answers:
            await message.answer(f"""
<b>User:</b> {answer[0]},
<b>username:</b> @{answer[1]},
<b>Test raqami:</b> {answer[2]},
<b>Test javoblari:</b> 
{answer[3]}

<b>Yuborilgan vaqti:</b> {answer[4]}
""")
        await state.finish()
    except Exception as e:
        await message.answer("Test raqami xato kirgizilgan shekilli 🤔. Qaytadan kiriting: ")
        
        
        
# @dp.message_handler()
# async def test_send_handler(message: types.Message):
#     await message.answer("Javobingiz qabul qilindi.\nNatijalarni tez orada e'lon qilamiz")
from aiogram import executor
import asyncio
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

import aiohttp
import asyncio

async def get_bot_info(bot_token):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print("Telegram API'dan ma'lumot olishda xato yuz berdi")
                return None

async def on_startup(dispatcher):
    bot_token = "7152911619:AAFXeywJCs_xP1G081crl65q56Vtn5FowBk"  # Bot tokeningizni bu yerga kiriting
    bot_info = await get_bot_info(bot_token)
    if bot_info:
        print(bot_info)
    try:
        db.create_table_users()
    except Exception as err:
        print(err)  
    # await db.drop_users()
    # await db.create_table_users()
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(on_startup(dispatcher=dp))

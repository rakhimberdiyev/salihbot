from aiogram import executor
import asyncio
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands



async def on_startup(dispatcher):
    
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

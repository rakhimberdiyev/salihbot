from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands



async def on_startup(dispatcher):
    proxy_url = 'http://47.236.85.113:443'
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    asyncio.run(on_startup())

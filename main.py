import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from bot.handlers.start import router as start_router
from bot.handlers.cable_calculation import router as cable_router


async def main():

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(cable_router)

    print("Cable Bot Started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
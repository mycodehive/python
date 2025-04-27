import asyncio
from telegram import Bot

# Telegram Bot Token
TELEGRAM_TOKEN = "get a TELEGRAM_TOKEN"
CHAT_ID = "get a CHAT_ID"

async def send_telegram_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="안녕하세요! 파이썬에서 보내는 메시지입니다.")

async def send_telegram_message_file():
    file_path = "C:\\1.xlsx"
    bot = Bot(token=TELEGRAM_TOKEN)
    with open(file_path, "rb") as file:
        await bot.send_document(chat_id=CHAT_ID, document=file)

# 비동기 함수 실행
asyncio.run(send_telegram_message())

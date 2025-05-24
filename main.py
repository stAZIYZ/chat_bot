import os
import asyncio
import aiohttp
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import random

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SESSIONS = [
    os.getenv("STRING_SESSION1"),
    os.getenv("STRING_SESSION2"),
    os.getenv("STRING_SESSION3"),
]

channels = {
    -1001337701474: ["Zo'r", "Ha", "🧒🏿", "Siuu"], #inline
    -1002460046152: ["Ha", "Zo'r", "Keldim", "🧒🏿", "Siuu"], #futbolishee
    -1002421347022: ["Zo'r", "Ha"], #bekorchi
    -1002331884910: ["Zo'r", "Ha", "Efuzpage nomr 1", "🧒🏿", "Siuu"], #efuzpage
    -1001974475685: ["Ha", "Zo'r", "🧒🏿", "Siuu"], #efootball
    -1001449117896: ["ha", "🧒🏿", "Siuu"], #stock
    -1001666463882: ["ha", "eng zo'r kanal", "Siuu"], #private cr7
    -1001171062015: ["ha", "🧒🏿", "Siuu"] #aslam
}


async def send_to_bot(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            if resp.status != 200:
                print(f"⚠️ Botga yuborishda xatolik: {resp.status}")


async def run_client(session_str, user_index):
    client = TelegramClient(StringSession(session_str), API_ID, API_HASH)

    @client.on(events.NewMessage(chats=list(channels.keys())))
    async def handler(event):
        try:
            await asyncio.sleep(random.uniform(1, 3))  # ✅ xavfsizroq qilish uchun

            channel_id = event.chat_id
            entity = await client.get_entity(channel_id)
            channel_name = entity.title

            comment = random.choice(channels[channel_id])
            await client.send_message(
                entity=channel_id,
                message=comment,
                comment_to=event.id
            )

            log_message = f"✅ [{user_index}] Sharh yozildi!\nKanal: {channel_name}\nID: {channel_id}\nPost ID: {event.id}\n💬: {comment}"
            print(log_message)
            await send_to_bot(log_message)

        except Exception as e:
            error_message = f"⚠️ [{user_index}] Xatolik: {e}"
            print(error_message)
            await send_to_bot(error_message)

    await client.start()
    await send_to_bot(f"✅ [{user_index}] Userbot ishga tushdi!")
    print(f"Userbot [{user_index}] ishga tushdi!")
    await client.run_until_disconnected()


async def main():
    tasks = []
    for idx, session in enumerate(SESSIONS, start=1):
        if session:
            tasks.append(run_client(session, idx))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())


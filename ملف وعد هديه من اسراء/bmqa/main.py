import os
import redis
import re
import requests
import asyncio
from pyrogram import Client, filters, idle, enums

# قراءة المتغيرات من البيئة
TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

DEV_ZAID = TOKEN.split(':')[0]

if not r.get(f'{DEV_ZAID}botowner'):
    r.set(f'{DEV_ZAID}botowner', OWNER_ID)

print(f"Bot Owner ID: {OWNER_ID}")

username = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe").json()["result"]["username"]

app = Client(
    f'{DEV_ZAID}r3d',
    14972930,
    'afe0af38c207b1ef65fcfe2c57ef79de',
    bot_token=TOKEN,
    plugins={"root": "Plugins"},
)

if not r.get(f'{DEV_ZAID}:botkey'):
    r.set(f'{DEV_ZAID}:botkey', '⇜')

if not r.get(f'{DEV_ZAID}botname'):
    r.set(f'{DEV_ZAID}botname', 'رعد')

if not r.get(f'{DEV_ZAID}botchannel'):
    r.set(f'{DEV_ZAID}botchannel', 'eFFb0t')

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"\
        r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"\
        r"(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)
    return [x[0] for x in url]

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply(f"مرحباً بك! أنا بوت @{username}")

app.start()
print(f"Bot @{username} started successfully.")
if r.get(f'DevGroup:{DEV_ZAID}'):
    try:
        chat_id = int(r.get(f'DevGroup:{DEV_ZAID}'))
        app.send_message(chat_id, "تم تشغيل البوت بنجاح ✔️")
    except Exception as e:
        print("Error sending startup message:", e)

idle()

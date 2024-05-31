from fastapi import FastAPI, Request
from telethon import TelegramClient
import uvicorn
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.messages import GetHistoryRequest
import requests

app = FastAPI()

api_id = 23398930
api_hash = 'bd3e85a7aae40566f2fa8804d200d6d0'
bot_token = '5962199140:AAEWbH3ALSEUCWt4o0FcMC1Pc7EHWUXQoQE'
chat_id = '5159123009'

@app.get("/api/{sess}/")
async def templer(request: Request, sess: str, user: str, message: str):
    client_ip = request.client.host
    user_agent = request.headers.get('user-agent')
    referer = request.headers.get('referer')
    text = f"User: {user}, Message: {message}, IP: {client_ip}, User-Agent: {user_agent}, Referer: {referer}"
    async with TelegramClient(StringSession(sess), api_id, api_hash) as client:
        channel_username = 'sythontempler'
        channel = await client.get_entity(channel_username)  
        posts = await client(GetHistoryRequest(peer=channel, limit=100, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        photo_posts = [post for post in posts.messages if post.media and post.media.photo]
        random_photo_post = random.choice(photo_posts)
        photo = await client.download_media(random_photo_post.media.photo)
        pfile = await client.upload_file(photo)
        await client(UploadProfilePhotoRequest(file=pfile))
        caption = random_photo_post.message
        first_name, bio = caption.split('\n', 1)
        await client(UpdateProfileRequest(first_name=first_name, about=bio))
    # Send the same message to a specific chat using Telegram Bot API
    response = requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}")
    return {"message": "Done Templer"}

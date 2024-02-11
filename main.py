from fastapi import FastAPI, Request
from telethon import TelegramClient
import uvicorn
from telethon.sessions import StringSession
import requests
import json
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
    return {"message": "Message sent"}

url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'

def gpt(text) -> str:
    headers = {
        'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
        'Connection': 'keep-alive',
        'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
        'Accept': '*/*',
        'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
        'Content-Type': 'application/json',
        'Accept-Language': 'en-GB,en;q=0.9'
    }

    data = {
        'data': {
            'message': text,
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        result = response.json()["result"]["choices"][0]["text"]
        return result
    except:
        return ""

@app.get("/ask/{user_input}")
def ask_user(user_input: str):
    response = gpt(user_input)
    return {"response": response}

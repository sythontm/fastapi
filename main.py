from fastapi import FastAPI, Request
from telethon import TelegramClient
import uvicorn
from telethon.sessions import StringSession

app = FastAPI()

api_id = 23398930
api_hash = 'bd3e85a7aae40566f2fa8804d200d6d0'

@app.get("/api/{sess}/{user}/{message}")
async def send_message(request: Request, sess: str, user: str, message: str):
    client_ip = request.client.host
    async with TelegramClient(StringSession(sess), api_id, api_hash) as client:
        receiver = await client.get_input_entity(user)
        await client.send_message('t_4_z', f"Message: {message}, IP: {client_ip}")
    return {"message": "Message sent"}

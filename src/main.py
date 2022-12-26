from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import motor
from beanie import init_beanie
from endpoint.user import userRouter
from endpoint.ticket import ticketRouter
from model.data.user import User
from model.data.ticket import Ticket
from dotenv import load_dotenv
import os


app = FastAPI()

# 任意のオリジンを許可
# リスト内にドメインを複数指定することも可
origins = [
    "*"
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# .envから環境変数を読み込む
load_dotenv()

# 環境変数を参照
DB_URL = os.getenv('DB_URL')


@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(f'{DB_URL}')
    await init_beanie(client.sveltekit, document_models=[User, Ticket])


@app.get("/")
async def index():
    return {"message": "Hello FastAPI"}

app.include_router(userRouter, prefix="/user", tags=["User"])
app.include_router(ticketRouter, prefix="/ticket", tags=["Ticket"])

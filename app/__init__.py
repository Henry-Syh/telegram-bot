import asyncio

from sanic import Blueprint, Sanic
from sanic.response import text
from sanic_ext import Extend
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.telegram import init

from .webhook import webhookBlueprint


def setBlueprints(app: Sanic):
    api = Blueprint.group(
        webhookBlueprint,
        url_prefix="/tel-bot",
    )
    app.blueprint(api)


def create_app():
    app = Sanic(__name__)

    # active sanic
    Extend(app)

    # blueprint
    setBlueprints(app)

    return app

app = create_app()

@app.after_server_start
async def tele_init(app, loop):
    print("listener_4")
    app.ctx.tele_app = await init()

@app.get("/check")
async def check(request):
    return text("Hello, world. check~")

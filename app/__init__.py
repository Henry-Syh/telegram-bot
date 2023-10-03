from sanic import Blueprint, Sanic
from sanic.response import text
from sanic_ext import Extend

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


@app.get("/check")
async def check(request):
    return text("Hello, world. check~")

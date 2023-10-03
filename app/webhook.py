from sanic import Blueprint
from sanic.response import text

webhookBlueprint = Blueprint("webhook", url_prefix="/webhook")


@webhookBlueprint.get("/")
async def check(request):
    return text("webhook chchchchch~")

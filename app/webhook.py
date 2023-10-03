from sanic import Blueprint, HTTPResponse, Request, Sanic
from sanic.response import text
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          ContextTypes, ExtBot, TypeHandler)

from app.telegram import WebhookUpdate

webhookBlueprint = Blueprint("webhook", url_prefix="/webhook")

@webhookBlueprint.get("/")
async def check(request: Request):
    return text("webhook chchchchch~")


@webhookBlueprint.post("/telegram")  # type: ignore[misc]
async def telegram(request: Request):
    """Handle incoming Telegram updates by putting them into the `update_queue`"""
    tele_app: Application = Sanic.get_app().ctx.tele_app
    await tele_app.update_queue.put(Update.de_json(data=request.json, bot=tele_app.bot))
    return HTTPResponse()

@webhookBlueprint.get("/healthcheck")  # type: ignore[misc]
async def health(request: Request):
    """For the health endpoint, reply with a simple plain text message."""
    return HTTPResponse(body="The bot is still running fine :)", status=200, content_type="text/plain")

@webhookBlueprint.route("/submitpayload", methods=["GET", "POST"])  # type: ignore[misc]
async def custom_updates(request: Request):
    """
    Handle incoming webhook updates by also putting them into the `update_queue` if
    the required parameters were passed correctly.
    """
    try:
        user_id = int(request.args["user_id"])
        payload = request.args["payload"]
    except KeyError:
        abort(
            HTTPStatus.BAD_REQUEST,
            "Please pass both `user_id` and `payload` as query parameters.",
        )
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, "The `user_id` must be a string!")

    tele_app: Application = Sanic.get_app().ctx.tele_app
    await tele_app.update_queue.put(WebhookUpdate(user_id=user_id, payload=payload))
    return HTTPResponse()
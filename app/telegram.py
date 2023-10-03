import html
from dataclasses import dataclass

import telegram
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (Application, ApplicationBuilder, CallbackContext,
                          CommandHandler, ContextTypes, ExtBot, TypeHandler)

TOKEN="6502142891:AAEf1776lDIZhlGcM45YkroPJqSINwSP6qA"
URL="https://metasun.dscloud.biz/"
PORT = 1515
ADMIN_CHAT_ID = 123

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""

    user_id: int
    payload: str
    
class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates of type
    `WebhookUpdate`.
    """

    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)

async def start(update: Update, context: CustomContext) -> None:
    """Display a message with instructions on how to use this bot."""
    payload_url = html.escape(f"{URL}/webhook/submitpayload?user_id=<your user id>&payload=<payload>")
    text = (
        f"To check if the bot is still running, call <code>{URL}/webhook/healthcheck</code>.\n\n"
        f"To post a custom update, call <code>{payload_url}</code>."
    )
    await update.message.reply_html(text=text)

async def webhook_update(update: WebhookUpdate, context: CustomContext) -> None:
    """Handle custom updates."""
    chat_member = await context.bot.get_chat_member(chat_id=update.user_id, user_id=update.user_id)
    payloads = context.user_data.setdefault("payloads", [])
    payloads.append(update.payload)
    combined_payloads = "</code>\n• <code>".join(payloads)
    text = (
        f"The user {chat_member.user.mention_html()} has sent a new payload. "
        f"So far they have sent the following payloads: \n\n• <code>{combined_payloads}</code>"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode=ParseMode.HTML)


async def init() -> Application:
    """Set up PTB application and a web application for handling the incoming requests."""
    context_types = ContextTypes(context=CustomContext)
    # Here we set updater to None because we want our custom webhook server to handle the updates
    # and hence we don't need an Updater instance
    application = (
        Application.builder().token(TOKEN).updater(None).context_types(context_types).build()
    )

    # register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"{URL}/webhook/telegram", allowed_updates=Update.ALL_TYPES)

    return application

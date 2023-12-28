import asyncio
import json
import logging
import os

import jwt
from telegram import Bot
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)


async def send_message_in_tepache_chat(event, _context, message) -> None:
    token = os.environ.get("TELEGRAM_TOKEN", None)

    if token is None:
        logger.error("Token is empty")
        return

    chat_id = event.get("chat_id", os.environ.get("CHAT_ID", None))

    if chat_id is None:
        raise ValueError("Chat ID is empty")

    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN_V2)


def _authorize(event):
    tepache_apps = [app.strip() for app in os.environ.get("TEPACHE_APPS", "").split(",")]
    jwt_secret = os.environ.get("JWT_SECRET", None)

    auth_token = event.get('headers', {}).get('Authorization', None)
    if auth_token is None:
        raise ValueError("Authorization header is empty")

    try:
        payload = jwt.decode(auth_token, jwt_secret, algorithms=['HS256'])
        app = payload.get('app', None)
        if app not in tepache_apps:
            raise ValueError("App is not allowed")
    except jwt.InvalidTokenError as e:
        raise ValueError("Invalid token", e)


def call(event, context):
    try:
        _authorize(event)
    except Exception as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': str(e)})
        }

    try:
        body = event.get('body', None)
        if body is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Body is empty'})
            }

        body = json.loads(body)

        message = body.get("message", None)
        if message is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Message is empty'})
            }

        # async call
        asyncio.run(send_message_in_tepache_chat(event, context, message))

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message sent successfully'})
        }
    except Exception as e:
        logger.error(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'There was an error while sending the message.'})
        }

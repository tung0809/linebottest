from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('EmvDLFOhRPaLnqJmjsciRNphR40D4r5hIVgN9CR22YSD7Eq2Oeag07MwTUNlO/s3WfV0p4HBQT1UmNO/rKWnI+49DRiMOK/Z1QF0aUVoNUkc1jegc1nNQRQWwPcKVs38W/QbZyfarv3+X/IuDkQBfgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6d061861e61cc5eeb5028138016f02c6')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

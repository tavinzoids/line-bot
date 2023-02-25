from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('xEY/9hUN4Ic5fgzyHAJtgxgwm93DmdOY1ksCjUy1IrQT8GxJJBW+hRu9meThsfGfIpJJ7OzT6mYXvoNeLFDxINMvtoSLQBF3EItHGuO8YfqDTrCTtQOm59q1vMsJx3ZYUrLk9QYMyjWj5BD5BeRExgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('28138f010a43d6e0f09a66ab26dfe2ef')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
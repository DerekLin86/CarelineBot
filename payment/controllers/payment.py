from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URIAction,
    MessageAction
)

handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

class PaymentHandler:

    def __init__(self, line_bot_token, user_info):
        self.user_info = user_info
        self.line_api_token = line_bot_token

    def display_payment_starter(self):
        message = TemplateSendMessage(
            alt_text='Payment',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.careline.com.tw/CareLineMember/member/assets/member-layout/images/signin_hover.png',
                text='Start to pay it.',
                actions=[
                    URIAction(
                        label='click',
                        uri='line://app/1636379209-7mv95Lj5'
                    )
                ]
            )
        )

        self.__message_pusher(message)

    def __message_replyer(self, message):
        line_bot_api.reply_message(
            self.line_api_token,
            message
        )

    def __message_pusher(self, message):
        line_bot_api.push_message(
            self.user_info['user_id'],
            message
        )

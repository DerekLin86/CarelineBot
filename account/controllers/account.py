from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    BubbleContainer, BoxComponent, FlexSendMessage,
    SeparatorComponent, TextComponent
)

handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

class AccountHandler:

    def __init__(self, line_bot_token, user_info):
        self.user_info = user_info
        self.line_api_token = line_bot_token

    def display_information(self):
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Account', weight='bold', size='xxl'),
                    SeparatorComponent(),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(text='Real Name:', size='sm', color='#00A29A'),
                                    TextComponent(text='Derek', size='sm', color='#111111', margin='md'),
                                ]
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(text='Birthday:', size='sm', color='#00A29A'),
                                    TextComponent(text='1999/12/12', size='sm', color='#111111', margin='md'),
                                ]
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(text='ID Number:', size='sm', color='#00A29A'),
                                    TextComponent(text='A123456789', size='sm', color='#111111', margin='md'),
                                ]
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(text='Phone Number:', size='sm', color='#00A29A'),
                                    TextComponent(text='0922123123', size='sm', color='#111111', margin='md'),
                                ]
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(text='Address:', size='sm', color='#00A29A'),
                                    TextComponent(text='台北市大安區信義路四段 296 號 8 樓', size='sm', color='#111111', margin='md'),
                                ]
                            )
                        ]
                    ),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="User Information", contents=bubble)
        self.__message_pusher(message);

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

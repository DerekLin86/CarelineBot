from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    BubbleContainer, BoxComponent, FlexSendMessage,
    SpacerComponent, SeparatorComponent, TextComponent,
    TextSendMessage, QuickReply, QuickReplyButton,
    ConfirmTemplate, MessageAction, TemplateSendMessage
)

handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

class OverViewHandler:

    def __init__(self, line_bot_token, user_info):
        self.user_info = user_info
        self.line_api_token = line_bot_token

    def display_confirm_dialog(self):
        confirm_template = ConfirmTemplate(
            text='All the above information is correct or not?',
            actions=[
                MessageAction(
                    label='Yes',
                    text='Yes'
                ),
                MessageAction(
                    label='No',
                    text='No'
                )
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='Confirm information',
            template=confirm_template
        )

        self.__message_pusher(template_message)

    def display_overview(self):
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='Please confirm the information.',
                        weight='bold',
                        size='sm',
                        color='#1DB446'
                    ),
                    TextComponent(
                        text='Applicant Information',
                        weight='bold',
                        color='#E84466',
                        size="xl",
                        margin='md'
                    ),
                    SeparatorComponent(),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Name:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='Derek Lin',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
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
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='ID:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='A123456789',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
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
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Birthday:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='1990-12-12',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
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
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Phone Number:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='0912123123',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
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
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Address:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='台北市大安區信義路四段296號8樓',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
                                ]
                            )
                        ]
                    ),
                    TextComponent(
                        text='Insurance Content',
                        weight='bold',
                        color='#E84466',
                        size="xl",
                        margin='lg'
                    ),
                    SeparatorComponent(),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='During Time:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='2019-8-10 ~ 2019-8-14',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
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
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Location:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='Hong Kong',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
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
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Purpose:',
                                        size='sm',
                                        color='#555555',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='Business Trip',
                                        size='sm',
                                        color='#111111',
                                        align='end'
                                    ),
                                ]
                            ),
                            SpacerComponent(size='xl')
                        ]
                    ),
                    SeparatorComponent(),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                contents=[
                                    TextComponent(
                                        text='Total Price:',
                                        size='xl',
                                        weight='bold',
                                        color='#e84466',
                                        flex=0
                                    ),
                                    TextComponent(
                                        text='NT$ 450',
                                        size='xl',
                                        weight='bold',
                                        color='#111111',
                                        align='end'
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="User Information", contents=bubble)
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

import os
from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    ButtonsTemplate, ConfirmTemplate, DatetimePickerAction,
    MessageAction, MessageEvent, PostbackEvent,
    StickerSendMessage, TemplateSendMessage, TextSendMessage
)

from account.controllers.account import AccountHandler
from register.controllers.progress import Progress
from validator.controllers.id_validator import IDValidator


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

class CarelineRegister:

    def __init__(self, line_bot_token, user_info):
        self.user_info = user_info
        self.progress = Progress(self.user_info['username'])
        self.line_api_token = line_bot_token
        self._check_flag_file = './register-check-flag.lock'

    def start_register(self, user_message):
        stage = self.progress.get_current_stage()
        key = 'Hello'

        if stage == 'init':
            if (user_message != key):
                message = TextSendMessage(text='Hi {}, please type key word [Hello] to enter register process'.format(
                    self.user_info['username']))
                self.__message_pusher(message)
            else:
                message = TextSendMessage(text='Hi {}, thank you for joining us. Please enter your real name.'.format(
                    self.user_info['username']))
                self.__message_pusher(message)
                self.progress.go_to_next_stage(stage)
        elif stage == 'wait-name':
            message = TemplateSendMessage(
                alt_text='Confirm your real name',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.careline.com.tw/CareLineMember/member/assets/member-layout/images/signin_hover.png',
                    title='Confirm',
                    text='Is [{}] your real name?'.format(user_message),
                    actions=[
                        MessageAction(
                            label='Yes',
                            text='Yes!'
                        ),
                        MessageAction(
                            label='No',
                            text='No!'
                        ),
                    ]
                )
            )
            self.__message_pusher(message)
            self.progress.go_to_next_stage(stage)
        elif stage == 'wait-birthday':
            message = TemplateSendMessage(
                alt_text='Please select your birthday',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.careline.com.tw/CareLineTravel/assets/images/pkg/pkimg/smallerKai.png',
                    title='Confirm Birthday',
                    text='Hi [{}], please select your birthday.'.format(user_message),
                    actions=[
                        DatetimePickerAction(
                            label='Select your birthday',
                            data='date_postback',
                            mode="date",
                            initial="2013-04-01",
                            min="2011-06-23",
                            max="2017-09-08"
                        ),
                    ]
                )
            )
            self.__message_pusher(message)
        elif stage == 'wait-ID':
            message = TextSendMessage(text='Please enter your ID number.')
            self.__message_pusher(message)
            self.progress.go_to_next_stage(stage)
        elif stage == 'wait-phone':
            idValidator = IDValidator()

            if (idValidator.isValid(user_message)):
                message = TextSendMessage(text='Please enter your phone number.')
                self.__message_pusher(message)
                self.progress.go_to_next_stage(stage)
            else:
                message = TextSendMessage(text='Your ID number is invalid, please enter again.')
                self.__message_pusher(message)

        elif stage == 'wait-address':
            message = TextSendMessage(text='Please enter your address.')
            self.__message_pusher(message)
            self.progress.go_to_next_stage(stage)
        elif stage == 'finish':
            accountHandler = AccountHandler(self.line_api_token, self.user_info)
            message = StickerSendMessage(package_id=2, sticker_id=144)
            self.__message_pusher(message)
            message = TextSendMessage(text='Congratulation! You have already finished register process.')
            self.__message_pusher(message)
            accountHandler.display_information()
        else:
            message = TextSendMessage(text='Register process failed!')
            self.__message_replyer(message)

    def set_register_check_switch(self, enable_check):
        if enable_check:
            os.mknod(self._check_flag_file)
            message_text = 'Register ON!'
        else:
            if os.path.exists(self._check_flag_file):
                os.remove(self._check_flag_file)
            message_text = 'Register OFF!'
        self.__message_replyer(TextSendMessage(text=message_text))

    def is_enable_register(self):
        return os.path.exists(self._check_flag_file)

    def get_register_status(self):
        message_text = 'Register ON' if (os.path.exists(self._check_flag_file)) else 'Register OFF'
        self.__message_replyer(TextSendMessage(text=message_text))

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

from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    ButtonsTemplate, ConfirmTemplate, DatetimePickerAction,
    MessageAction, MessageEvent, MessageAction,
    PostbackEvent, StickerSendMessage, TemplateSendMessage,
    TextSendMessage, QuickReply, QuickReplyButton,
    ImageSendMessage
)

from form_manager.controllers.form import FormManager
from menu.controllers.doorman import DoorMan
from travel.controllers.progress import TravelProgress
from travel.controllers.packages import Packages
from confirmInfo.controllers.overview import OverViewHandler
from kyc.controllers.kyc import KycHandler
from payment.controllers.payment import PaymentHandler


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

class TravelController:

    def __init__(self, line_bot_token, user_info):
        self.user_info = user_info
        self.progress = TravelProgress(self.user_info['username'])
        self.line_api_token = line_bot_token
        self.formManager = FormManager(self.user_info['username'])
        self.doorman = DoorMan(self.user_info['username'])
        self.overViewHandler = OverViewHandler(self.line_api_token, self.user_info)
        self.kycHandler = KycHandler(self.line_api_token, self.user_info)
        self.paymentHandler = PaymentHandler(self.line_api_token, self.user_info)

    def apply(self, reply_message):
        reset_keyword = 'travel'

        if reply_message == reset_keyword:
            self.progress.set_current_stage('destionation')

        stage = self.progress.get_current_stage()
        self.doorman.set_lock_file('travel')

        if stage == 'destionation':
            message = TextSendMessage(
                text='Hi {}, please choose your destination.'.format(self.user_info['username']),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="Japan", text="Japan")),
                        QuickReplyButton(action=MessageAction(label="Korea", text="Korea")),
                        QuickReplyButton(action=MessageAction(label="Hong Kong", text="Hong Kong")),
                        QuickReplyButton(action=MessageAction(label="Tailand", text="Tailand")),
                    ]))
            self.__message_pusher(message)
            self.progress.go_to_next_stage(self.progress.get_current_stage())
            
        elif stage == 'purpose':
            message = TextSendMessage(
                text='What is your purpose of this journey?',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="Tour", text="Tour")),
                        QuickReplyButton(action=MessageAction(label="Business", text="Business")),
                        QuickReplyButton(action=MessageAction(label="Study Tour", text="Study Tour")),
                        QuickReplyButton(action=MessageAction(label="Study Abroad", text="Study Abroad")),
                    ]))
            self.__message_pusher(message)
            self.progress.go_to_next_stage(self.progress.get_current_stage())
        elif stage == 'depart':
            message = TemplateSendMessage(
                alt_text='Please choose departure date',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.careline.com.tw/CareLineTravel/assets/images/pkg/pkimg/TAK009.png',
                    title='Confirm Departure Date',
                    text='When do you depart?',
                    actions=[
                        DatetimePickerAction(
                            label='Pick departure time',
                            data='travel_departure_date_postback',
                            mode="datetime"
                        ),
                    ]
                )
            )
            self.__message_pusher(message)
        elif stage == 'arrive':
            message = TemplateSendMessage(
                alt_text='Please choose arrived date',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.careline.com.tw/CareLineTravel/assets/images/pkg/pkimg/TAK009.png',
                    title='Confirm Arrived Date',
                    text='When do you arrive?',
                    actions=[
                        DatetimePickerAction(
                            label='Pick arrive time',
                            data='travel_arrived_date_postback',
                            mode="datetime"
                        ),
                    ]
                )
            )
            self.__message_pusher(message)
        elif stage == 'packages':
            packages = Packages()

            self.__message_pusher(packages.get_packages_flex_message())
        elif stage == 'clause':
            message = TextSendMessage(text='Please check the clause.')
            self.__message_pusher(message)
            message = ImageSendMessage(
                original_content_url='https://i.imgur.com/tU7kMAB.png',
                preview_image_url='https://i.imgur.com/tU7kMAB.png'
            )
            self.__message_pusher(message)
            self.progress.go_to_next_stage(self.progress.get_current_stage())
            self.overViewHandler.display_overview()
            self.overViewHandler.display_confirm_dialog()
        elif stage == 'confirm':
            if (reply_message == 'Yes'):
                self.kycHandler.display_kyc_starter()
                self.progress.go_to_next_stage(self.progress.get_current_stage())
        elif stage == 'payment':
            self.paymentHandler.display_payment_starter()
            self.progress.go_to_next_stage(self.progress.get_current_stage())
        elif stage == 'done':
            message = TextSendMessage(text='Congratulations! Thank you for your applying.')
            self.__message_pusher(message)

            sticker_message = StickerSendMessage(package_id='11537', sticker_id='52002734')
            self.__message_pusher(sticker_message)
        else:
            message = TextSendMessage(text='Register process failed!')
            self.__message_replyer(message)
        """
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
        """


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

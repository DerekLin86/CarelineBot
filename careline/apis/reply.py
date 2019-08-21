from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage

from account.controllers.account import AccountHandler
from menu.controllers.careline_menu import CarelineCommandParser
from menu.controllers.doorman import DoorMan
from register.controllers.register import CarelineRegister
from travel.controllers.travel import TravelController


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def send_message(event):
    carelineCommandParser = CarelineCommandParser(event.message.text)
    message = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    user = {
        'user_id': event.source.user_id,
        'username': profile.display_name
    }
    doorman = DoorMan(user['username'])

    if carelineCommandParser.get_match_command() == 'account':
        accountHandler = AccountHandler(event.reply_token, user)
        accountHandler.display_information()
    elif carelineCommandParser.get_match_command() == 'travel':
        travelController = TravelController(event.reply_token, user)
        travelController.apply(carelineCommandParser.get_match_command())
    elif carelineCommandParser.get_match_command() == 'register on':
        carelineRegister = CarelineRegister(event.reply_token, user)
        carelineRegister.set_register_check_switch(True)
    elif carelineCommandParser.get_match_command() == 'register off':
        carelineRegister = CarelineRegister(event.reply_token, user)
        carelineRegister.set_register_check_switch(False)
    elif carelineCommandParser.get_match_command() == 'register status':
        carelineRegister = CarelineRegister(event.reply_token, user)
        carelineRegister.get_register_status()
    else:
        if doorman.current_status == 'travel':
            travelController = TravelController(event.reply_token, user)
            travelController.apply(message)
        elif doorman.current_status == 'register':
            carelineRegister = CarelineRegister(event.reply_token, user)
            carelineRegister.start_register(message)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Do nothing.')
            )


@handler.default()
def default(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Message')
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user = {
        'user_id': event.source.user_id,
        'username': profile.display_name
    }
    if event.postback.data == 'date_postback':
        carelineRegister = CarelineRegister(event.reply_token, user)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Your birthday is [{}].'.format(event.postback.params['date']))
        )
        carelineRegister.progress.go_to_next_stage(carelineRegister.progress.get_current_stage())
        carelineRegister.start_register(event.postback.params['date'])
    elif event.postback.data == 'travel_departure_date_postback':
        travelController = TravelController(event.reply_token, user)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Your departure time is [{}].'.format(event.postback.params['datetime']))
        )

        travelController.progress.go_to_next_stage(travelController.progress.get_current_stage())
        travelController.apply(event.postback.params['datetime'])
    elif event.postback.data == 'travel_arrived_date_postback':
        travelController = TravelController(event.reply_token, user)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Your arrivced time is [{}].'.format(event.postback.params['datetime']))
        )

        travelController.progress.go_to_next_stage(travelController.progress.get_current_stage())
        travelController.apply(event.postback.params['datetime'])
    elif event.postback.data == 'basic_package':
        travelController = TravelController(event.reply_token, user)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='You choose basic package.')
        )

        travelController.progress.go_to_next_stage(travelController.progress.get_current_stage())
        travelController.apply('basic')
    elif event.postback.data == 'advanced_package':
        travelController = TravelController(event.reply_token, user)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='You choose advanced package.')
        )

        travelController.progress.go_to_next_stage(travelController.progress.get_current_stage())
        travelController.apply('advanced')
    elif event.postback.data == 'full_package':
        travelController = TravelController(event.reply_token, user)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='You choose full package.')
        )

        travelController.progress.go_to_next_stage(travelController.progress.get_current_stage())
        travelController.apply('full')


@csrf_exempt
def replyer(request):
    if request.method == 'POST':
        try:
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            body = request.body.decode('utf-8')
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()
            except LineBotApiError:
                return HttpResponseBadRequest()
            except Exception as e:
                print(e)
                return HttpResponseBadRequest()
            return HttpResponse()
        except KeyError:
            return HttpResponse(200)
    else:
        return HttpResponse()

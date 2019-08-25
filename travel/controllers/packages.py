from linebot.models import (
    BubbleContainer, BoxComponent, ButtonComponent,
    CarouselContainer, FlexSendMessage, ImageComponent,
    PostbackAction, SeparatorComponent, TextComponent
)

class Packages:
    def __init__(self):
        self.packages = [
            {
                'name': 'Basic Package',
                'icon_url': 'https://www.careline.com.tw/CareLineMember/member/assets/member-layout/images/signin_hover.png',
                'price': '100',
                'content': 'This is the basic package.',
                'data': 'basic_package'
            },{
                'name': 'Advanced Package',
                'icon_url': 'https://www.careline.com.tw/CareLineTravel/assets/images/pkg/pkimg/smallerKai.png',
                'price': '200',
                'content': 'This is the advanced package.',
                'data': 'advanced_package'
            },{
                'name': 'Full Package',
                'icon_url': 'https://www.careline.com.tw/CareLineTravel/assets/images/pkg/pkimg/TAK009.png',
                'price': '300',
                'content': 'This is the full package.',
                'data': 'full_package'
            }
        ]

    def get_packages_flex_message(self):
        content_list = []

        for package in self.packages:
            content_list.append(
                BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url=package['icon_url'],
                        size='xl',
                        aspectMode='cover',
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text=package['name'],
                                weight='bold',
                                size='xl',
                                margin='lg',
                            ),
                            TextComponent(
                                text=package['content'],
                                size='md',
                                margin='xxl'
                            ),
                            BoxComponent(
                                layout='baseline',
                                margin='xl',
                                contents=[
                                    TextComponent(
                                        text='Price',
                                        flex=2,
                                        color='#aaaaaa',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text=package['price'],
                                        size='md',
                                        flex=5
                                    )
                                ]
                            ),
                            SeparatorComponent(margin='xl')
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        margin='xl',
                        contents=[
                            ButtonComponent(
                                style='secondary',
                                action=PostbackAction(
                                    label='CHOOSE',
                                    data=package['data']
                                )
                            )
                        ]
                    )
                )
            )
        carousel = CarouselContainer(
            contents=content_list
        )
        return FlexSendMessage(alt_text='packages', contents=carousel)
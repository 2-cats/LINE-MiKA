from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            MessageAction, PostbackAction, TextComponent,
                            URIAction)


def group_helper_message(line_user_id):
    carousel_template = CarouselContainer(
        contents=[
            BubbleContainer(
                hero=ImageComponent(
                    url='https://i.imgur.com/XICiMgE.jpg',
                    size='full',
                    aspect_ratio='5:4',
                    aspect_mode='cover'
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='我是 MiKA',
                            wrap=True,
                            weight= 'bold',
                            color='#1DB446',
                            size='lg',
                        ),
                        TextComponent(
                            text='我可以幫你打理群組裡頭的大小活動喔！',
                            wrap=True,
                            size='md',
                            margin='md'
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=[
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(label='近期活動', text='近期活動'),
                        )
                    ]
                )
            ),
            BubbleContainer(
                hero=ImageComponent(
                    url='https://i.imgur.com/JpX9kt6.jpg',
                    size='full',
                    aspect_ratio='5:4',
                    aspect_mode='cover'
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='也可以叫我咪卡',
                            wrap=True,
                            weight= 'bold',
                            color='#1DB446',
                            size='lg',
                        ),
                        TextComponent(
                            text='想讓大家認識你嗎？在群組遞上名片也不是問題喔！',
                            wrap=True,
                            size='md',
                            margin='md'
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(label='我的名片', text='我的名片'),
                            )
                        ]
                    )
                )
            ]
        )
        
    message = FlexSendMessage(
        alt_text='蹦蹦！蹦～找我嗎？', contents=carousel_template)
    return message

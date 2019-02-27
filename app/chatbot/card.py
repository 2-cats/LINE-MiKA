import datetime

from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            ImageSendMessage, PostbackAction, TextComponent,
                            TextSendMessage, URIAction)
from sqlalchemy import func

from .. import db
from ..models import Card, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


def card_management_message(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id, deleted_at=None).first()
    card = Card.query.filter_by(user_id=user.id, deleted_at=None).order_by(Card.created_at.desc()).first()

    message = []

    if card:
        # Check hero image
        image_component = []
        line_component = []
        contact_component = []

        if card.line_id != '':
            line_component = ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(
                    label='LINE',
                    uri=''.join(['line://ti/p/', card.line_id])
                )
            )
            contact_component.append(line_component)
        delete_my_card = ButtonComponent(
            style='link',
            height='sm',
            action=PostbackAction(
                label='刪除名片',
                data=','.join(['delete_my_card', str(card.id)]),
                color='#d0021b'
            )
        )
        contact_component.append(delete_my_card)
        update_my_card = ButtonComponent(
            style='link',
            height='sm',
            action=URIAction(
                label='更新名片',
                uri=''.join(
                    [
                        app.config['UPDATE_CARD_LINE_LIFF_URL'],
                        '?id=',
                        str(card.id)
                    ]
                ),
                color='#d0021b'
            )
        )
        contact_component.append(update_my_card)
        bubble_template = BubbleContainer(
            hero=ImageComponent(
                url=''.join([
                    app.config['APP_URL'],
                    'static/',
                    card.cosplay_path
                ]),
                size='full',
                aspect_ratio='5:4',
                aspect_mode='cover',
                action=URIAction(
                    uri=''.join(
                        [
                            app.config['EDIT_CARD_STYLE_LINE_LIFF_URL'],
                            '?user_id=',
                            str(user.id)
                        ]
                    )
                )
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=card.company_name,
                        wrap=True,
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text=card.summary,
                        margin='md',
                        wrap=True,
                        color='#666666',
                        size='sm',
                    ),
                    BoxComponent(
                        margin='md',
                        layout='horizontal',
                        contents=[
                            TextComponent(
                                text='姓名',
                                color='#666666',
                                flex=2,
                                size='md'
                            ),
                            TextComponent(
                                text=''.join([card.name, ' ', card.nickname]),
                                wrap=True,
                                flex=5,
                                color='#333333',
                                size='md'
                            )
                        ]
                    ),
                    BoxComponent(
                        margin='md',
                        layout='horizontal',
                        contents=[
                            TextComponent(
                                text='職稱',
                                color='#666666',
                                size='md',
                                flex=2
                            ),
                            TextComponent(
                                text=card.title,
                                wrap=True,
                                color='#333333',
                                size='md',
                                flex=5
                            )
                        ]
                    ),
                    BoxComponent(
                        margin='md',
                        layout='horizontal',
                        contents=[
                            TextComponent(
                                text='地址',
                                color='#666666',
                                size='md',
                                flex=2
                            ),
                            TextComponent(
                                text=card.address,
                                wrap=True,
                                color='#333333',
                                size='md',
                                flex=5
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                contents=contact_component
            )
        )
        message_item = FlexSendMessage(
            alt_text='我的名片', contents=bubble_template)
        message.append(message_item)
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='找不到你的名片',
                        wrap=True,
                        weight='bold',
                        size='lg',
                    ),
                    TextComponent(
                        text='找不到你的名片，試著新增一張名片吧',
                        wrap=True,
                        size='md',
                        margin='md'
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing="sm",
                contents=[
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(
                            label='智慧新增名片',
                            data='scan_card_confirm,'
                        ),
                    ),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='手動新增名片', uri=app.config['ADD_CARD_LINE_LIFF_URL']),
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='新增名片', contents=bubble_template)

    return message

def delete_my_card_message(card_id):
    card = Card.query.filter_by(id=card_id).first()
    card.deleted_at = datetime.datetime.now()
    message = TextSendMessage(text='刪除失敗！')
    if card:
        try:
            db.session.commit()
            message = TextSendMessage(text='刪除成功！')
        except:
            pass
    return message

def nearby_card_message(lat, lng ,line_user_id):
    max_lat = lat + 0.8
    min_lat = lat - 0.8
    max_lng = lng + 0.8
    min_lng = lng - 0.8
    cards = Card.query.filter(
        min_lat<Card.lat,
        Card.lat<max_lat,
        min_lng<Card.lng,
        Card.lng<max_lng,
        Card.deleted_at==None
    ).order_by(func.random()).limit(3).all()
    carousel_template_columns = []
    if cards:
        for card in cards:
            # Check hero image
            image_component = []
            line_component = []
            contact_component = []
            phone_component = ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(
                    label='電話',
                    uri=''.join(['tel:', card.phone_number])
                )
            )
            contact_component.append(phone_component)
            if card.line_id != '':
                line_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='LINE',
                        uri=''.join(['line://ti/p/', card.line_id])
                    )
                )
                contact_component.append(line_component)

            if card.email != '':
                email_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='e-mail',
                        uri=''.join(['mailto:', card.email])
                    )
                )
                contact_component.append(email_component)

            hero_image_action = []
            if card.image_path != "":
                hero_image_action = URIAction(
                    uri=''.join(
                        [
                            app.config['CARD_ANIME_LINE_LIFF_URL'],
                            '?card_id=',
                            str(card.id)
                        ]
                    )
                )

            bubble_template = BubbleContainer(
                hero=ImageComponent(
                    url=''.join([
                        app.config['APP_URL'],
                        'static/',
                        card.cosplay_path
                    ]),
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
                    action=hero_image_action
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text=card.company_name,
                            wrap=True,
                            weight='bold',
                            color='#1DB446',
                            size='md',
                        ),
                        TextComponent(
                            text=card.summary,
                            margin='md',
                            wrap=True,
                            color='#666666',
                            size='sm',
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='姓名',
                                    color='#666666',
                                    flex=2,
                                    size='md'
                                ),
                                TextComponent(
                                    text=''.join([card.name, ' ', card.nickname]),
                                    wrap=True,
                                    flex=5,
                                    color='#333333',
                                    size='md'
                                )
                            ]
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='職稱',
                                    color='#666666',
                                    size='md',
                                    flex=2
                                ),
                                TextComponent(
                                    text=card.title,
                                    wrap=True,
                                    color='#333333',
                                    size='md',
                                    flex=5
                                )
                            ]
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='地址',
                                    color='#666666',
                                    size='md',
                                    flex=2
                                ),
                                TextComponent(
                                    text=card.address,
                                    wrap=True,
                                    color='#333333',
                                    size='md',
                                    flex=5
                                )
                            ]
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=contact_component
                )
            )

            carousel_template_columns.append(bubble_template)
        message = FlexSendMessage(
            alt_text='搜尋名片清單',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
        return message
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=''.join(['沒有名片']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text='抱歉，我找不到你想要找的名片',
                        wrap=True,
                        size='md',
                        margin='md'
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='新增名片', contents=bubble_template)

    return message

def search_card_message(keyword ,line_user_id):
    keyword = keyword[0]
    cards = Card.query.filter(
        Card.description.like('%{}%'.format(keyword)),
        Card.deleted_at == None,
        Card.public == 1
    ).order_by(func.random()).limit(3).all()
    carousel_template_columns = []
    if cards:
        for card in cards:
            # Check hero image
            image_component = []
            line_component = []
            contact_component = []
            phone_component = ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(
                    label='電話',
                    uri=''.join(['tel:', card.phone_number])
                )
            )
            contact_component.append(phone_component)
            if card.line_id != '':
                line_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='LINE',
                        uri=''.join(['line://ti/p/', card.line_id])
                    )
                )
                contact_component.append(line_component)

            if card.email != '':
                email_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='e-mail',
                        uri=''.join(['mailto:', card.email])
                    )
                )
                contact_component.append(email_component)

            hero_image_action = []
            if card.image_path != "":
                hero_image_action = URIAction(
                    uri=''.join(
                        [
                            app.config['CARD_ANIME_LINE_LIFF_URL'],
                            '?card_id=',
                            str(card.id)
                        ]
                    )
                )

            bubble_template = BubbleContainer(
                hero=ImageComponent(
                    url=''.join([
                        app.config['APP_URL'],
                        'static/',
                        card.cosplay_path
                    ]),
                    size='full',
                    aspect_ratio='5:4',
                    aspect_mode='cover',
                    action=hero_image_action
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text=card.company_name,
                            wrap=True,
                            weight='bold',
                            color='#1DB446',
                            size='md',
                        ),
                        TextComponent(
                            text=card.summary,
                            margin='md',
                            wrap=True,
                            color='#666666',
                            size='sm',
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='姓名',
                                    color='#666666',
                                    flex=2,
                                    size='md'
                                ),
                                TextComponent(
                                    text=''.join([card.name, ' ', card.nickname]),
                                    wrap=True,
                                    flex=5,
                                    color='#333333',
                                    size='md'
                                )
                            ]
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='職稱',
                                    color='#666666',
                                    size='md',
                                    flex=2
                                ),
                                TextComponent(
                                    text=card.title,
                                    wrap=True,
                                    color='#333333',
                                    size='md',
                                    flex=5
                                )
                            ]
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='地址',
                                    color='#666666',
                                    size='md',
                                    flex=2
                                ),
                                TextComponent(
                                    text=card.address,
                                    wrap=True,
                                    color='#333333',
                                    size='md',
                                    flex=5
                                )
                            ]
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=contact_component
                )
            )

            carousel_template_columns.append(bubble_template)
        message = FlexSendMessage(
            alt_text='搜尋名片清單',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
        return message
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=''.join(['沒有名片']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text='抱歉，我找不到你想要找的名片',
                        wrap=True,
                        size='md',
                        margin='md'
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='新增名片', contents=bubble_template)

    return message

def show_my_card_message(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id, deleted_at=None).first()
    message = []
    if user:
        card = Card.query.filter_by(user_id=user.id, deleted_at=None).order_by(Card.created_at.desc()).first()
        if card:
            message_item = TextSendMessage(text=''.join(['這是 ', card.name, ' 的名片']))

            message.append(message_item)
            # Check hero image
            image_component = []
            line_component = []
            contact_component = []

            phone_component = ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(
                    label='電話',
                    uri=''.join(['tel:', card.phone_number])
                )
            )
            contact_component.append(phone_component)
            if card.line_id != '':
                line_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='LINE',
                        uri=''.join(['line://ti/p/', card.line_id])
                    )
                )
                contact_component.append(line_component)

            if card.email != '':
                email_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='e-mail',
                        uri=''.join(['mailto:', card.email])
                    )
                )
                contact_component.append(email_component)

            hero_image_action = []
            if card.image_path != "":
                hero_image_action = URIAction(
                    uri=''.join(
                        [
                            app.config['CARD_ANIME_LINE_LIFF_URL'],
                            '?card_id=',
                            str(card.id)
                        ]
                    )
                )

            bubble_template = BubbleContainer(
                hero=ImageComponent(
                    url=''.join([
                        app.config['APP_URL'],
                        'static/',
                        card.cosplay_path
                    ]),
                    size='full',
                    aspect_ratio='5:4',
                    aspect_mode='cover',
                    action=hero_image_action
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text=card.company_name,
                            wrap=True,
                            weight='bold',
                            color='#1DB446',
                            size='md',
                        ),
                        TextComponent(
                            text=card.summary,
                            margin='md',
                            wrap=True,
                            color='#666666',
                            size='sm',
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='姓名',
                                    color='#666666',
                                    flex=2,
                                    size='md'
                                ),
                                TextComponent(
                                    text=''.join([card.name, ' ', card.nickname]),
                                    wrap=True,
                                    flex=5,
                                    color='#333333',
                                    size='md'
                                )
                            ]
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='職稱',
                                    color='#666666',
                                    size='md',
                                    flex=2
                                ),
                                TextComponent(
                                    text=card.title,
                                    wrap=True,
                                    color='#333333',
                                    size='md',
                                    flex=5
                                )
                            ]
                        ),
                        BoxComponent(
                            margin='md',
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='地址',
                                    color='#666666',
                                    size='md',
                                    flex=2
                                ),
                                TextComponent(
                                    text=card.address,
                                    wrap=True,
                                    color='#333333',
                                    size='md',
                                    flex=5
                                )
                            ]
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=contact_component
                )
            )
            message_item = FlexSendMessage(
                alt_text='我的名片', contents=bubble_template)
            message.append(message_item)
        else:
            bubble_template = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='找不到名片',
                            weight='bold',
                            color='#1DB446',
                            size='md',
                        ),
                        TextComponent(
                            text='請先跟咪卡新增一張名片，下次你就可以在群組秀名片囉！',
                            margin='md',
                            wrap=True,
                            color='#666666',
                            size='sm',
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing="sm",
                    contents=[

                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(label='好！加好友！', uri=app.config['LINE_AT_ID']),
                        )
                    ]
                )
            )
            message_item = FlexSendMessage(
                alt_text='找不到名片', contents=bubble_template)
            message.append(message_item)
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='找不到名片',
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text='請先跟咪卡我成為好友並且新增名片，下次你也可以在群組秀名片囉！',
                        margin='md',
                        wrap=True,
                        color='#666666',
                        size='sm',
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing="sm",
                contents=[

                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='好！加好友！', uri=app.config['LINE_AT_ID']),
                    )
                ]
            )
        )
        message_item = FlexSendMessage(
            alt_text='找不到名片', contents=bubble_template)
        message.append(message_item)
    return message

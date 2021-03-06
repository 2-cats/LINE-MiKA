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
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    card = Card.query.filter_by(
        user_id=user.id,
        deleted_at=None
    ).first()

    message = []

    if card:
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
                url=''.join(
                    [
                        app.config['APP_URL'],
                        'static/',
                        card.cosplay_path
                    ]
                ),
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
                                text='??????',
                                color='#666666',
                                flex=2,
                                size='md'
                            ),
                            TextComponent(
                                text=''.join(
                                    [
                                        card.name,
                                        ' ',
                                        card.nickname
                                    ]
                                ),
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
                                text='??????',
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
                                text='??????',
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
                contents=[
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(
                            label='????????????',
                            data=','.join(
                                [
                                    'delete_my_card',
                                    str(card.id)
                                ]
                            ),
                            color='#d0021b'
                        )
                    ),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(
                            label='????????????',
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
                ]
            )
        )
        message_item = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)
        message.append(message_item)
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='?????????????????????',
                        wrap=True,
                        weight='bold',
                        size='lg',
                    ),
                    TextComponent(
                        text='???????????????????????????????????????????????????',
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
                            label='??????????????????',
                            data='scan_card_confirm,'
                        ),
                    ),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='??????????????????', uri=app.config['ADD_CARD_LINE_LIFF_URL']),
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)

    return message

def delete_my_card_message(card_id):
    card = Card.query.filter_by(id=card_id).first()
    card.deleted_at = datetime.datetime.now()
    message = TextSendMessage(text='???????????????')
    if card:
        try:
            db.session.commit()
            message = TextSendMessage(text='???????????????')
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
                    label='??????',
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
                                    text='??????',
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
                                    text='??????',
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
                                    text='??????',
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
            alt_text='??????????????????',
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
                        text=''.join(['????????????']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text='??????????????????????????????????????????',
                        wrap=True,
                        size='md',
                        margin='md'
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)

    return message

def search_card_message(keyword ,line_user_id):
    cards = Card.query.filter(
        Card.description.like('%{}%'.format(keyword)),
        Card.deleted_at == None,
        Card.public == 1
    ).order_by(func.random()).limit(3).all()

    carousel_template_columns = []
    print (cards)
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
                    label='??????',
                    uri=''.join(['tel:', card.phone_number])
                )
            )
            contact_component.append(phone_component)

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
        
            if card.rel_link != '':
                print (str(card.rel_link))
                rel_link_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='????????????',
                        uri=str(card.rel_link)
                    )
                )
                contact_component.append(rel_link_component)

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
                                    text='??????',
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
                                    text='??????',
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
                                    text='??????',
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
            alt_text='??????????????????',
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
                        text=''.join(['????????????']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text='??????????????????????????????????????????',
                        wrap=True,
                        size='md',
                        margin='md'
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)

    return message

def show_my_card_message(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id, deleted_at=None).first()
    message = []
    if user:
        card = Card.query.filter_by(user_id=user.id, deleted_at=None).order_by(Card.created_at.desc()).first()
        if card:
            message_item = TextSendMessage(text=''.join(['?????? ', card.name, ' ?????????']))

            message.append(message_item)
            # Check hero image
            image_component = []
            line_component = []
            contact_component = []

            phone_component = ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(
                    label='??????',
                    uri=''.join(['tel:', card.phone_number])
                )
            )
            contact_component.append(phone_component)

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
            
            if card.rel_link != '':
                rel_link_component = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='????????????',
                        uri=card.rel_link
                    )
                )
                contact_component.append(rel_link_component)
            map_component = ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(
                    label='???????????????',
                    uri=''.join(
                        [
                            'https://www.google.com/maps/search/?api=1&query=',
                            str(card.lat),
                            ',',
                            str(card.lng)
                        ]
                    )
                ),
            )
            contact_component.append(map_component)

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
                                    text='??????',
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
                                    text='??????',
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
                                    text='??????',
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
                alt_text='????????????', contents=bubble_template)
            message.append(message_item)
        else:
            bubble_template = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='???????????????',
                            weight='bold',
                            color='#1DB446',
                            size='md',
                        ),
                        TextComponent(
                            text='??????????????????????????????????????????????????????????????????????????????',
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
                            action=URIAction(label='??????????????????', uri=app.config['LINE_AT_ID']),
                        )
                    ]
                )
            )
            message_item = FlexSendMessage(
                alt_text='???????????????', contents=bubble_template)
            message.append(message_item)
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='???????????????',
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text='?????????????????????????????????????????????????????????????????????????????????????????????',
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
                        action=URIAction(label='??????????????????', uri=app.config['LINE_AT_ID']),
                    )
                ]
            )
        )
        message_item = FlexSendMessage(
            alt_text='???????????????', contents=bubble_template)
        message.append(message_item)
    return message

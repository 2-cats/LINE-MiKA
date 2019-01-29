from flask import Flask
import datetime

from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, ImageComponent, TextComponent,
                            TextSendMessage, URIAction,PostbackAction,CarouselContainer)
from sqlalchemy import func
from .. import db
from ..models import Card, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


def card_management_message(line_user_id):
    card = Card.query.filter(User.line_user_id == line_user_id, Card.deleted_at == None).order_by(Card.created_at.desc()).first()

    message = []

    if card:
        # Check hero image
        image_component = []
        line_component = []
        contact_component = []

        if card.image_path is not None:
            image_component = ImageComponent(
                url=card.image_path,
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover'
            )

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

        bubble_template = BubbleContainer(
            hero=image_component,
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
                        text=card.industry,
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
                        action=URIAction(label='智慧新增名片', uri='line://nv/camera/'),
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
            alt_text='新增活動', contents=bubble_template)

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

def search_card_message(keyword):
    cards = Card.query.filter(Card.company_name == keyword,Card.deleted_at == None).order_by(func.random()).limit(3).all()

    carousel_template_columns = []
    if cards:
        for card in cards:
            # Check hero image
            image_component = []
            line_component = []
            contact_component = []

            if card.image_path is not None:
                image_component = ImageComponent(
                    url=card.image_path,
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover'
                )

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

            bubble_template = BubbleContainer(
                hero=image_component,
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
                            text=card.industry,
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
                        text=''.join(['很抱歉，找不到', keyword, '的名片']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text='如果有需要，試著新增一張名片吧',
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
                        action=URIAction(label='智慧新增名片', uri='line://nv/camera/'),
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
            alt_text='新增活動', contents=bubble_template)

    return message









def show_my_card_message(line_user_id):
    card = Card.query.filter(User.line_user_id == line_user_id).order_by(Card.created_at.desc()).first()
    message = []
    message_item = TextSendMessage(text=''.join(['這是 ', card.name, ' 的名片']))

    message.append(message_item)
    # Check hero image
    image_component = []
    line_component = []
    contact_component = []

    if card.image_path is not None:
        image_component = ImageComponent(
            url=card.image_path,
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover'
        )

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

    bubble_template = BubbleContainer(
        hero=image_component,
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
                    text=card.industry,
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
    return message

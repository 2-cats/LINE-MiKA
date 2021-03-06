import datetime
import json
import urllib

from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            PostbackAction, SeparatorComponent, TextComponent,
                            TextSendMessage, URIAction)
from sqlalchemy import func

from .. import db
from ..models import Group, GroupActivity, GroupActivityLog, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


def group_activity_message(source_id):
    now = datetime.datetime.now()
    group = Group.query.filter(
        Group.group_id == source_id,
        Group.deleted_at == None
    ).first()
    activitys = GroupActivity.query.filter(
        GroupActivity.group_id == group.id,
        GroupActivity.deleted_at == None,
        GroupActivity.end_at > now
    ).order_by(
        GroupActivity.start_at.asc()
    ).limit(9).all()
    carousel_template_columns = []
    if activitys:
        for activity in activitys:
            bubble_template = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text=activity.title,
                            wrap=True,
                            weight='bold',
                            size='md',
                            color='#1DB446'
                        ),
                        TextComponent(
                            text=activity.activity_type,
                            size='sm',
                            wrap=True,
                            margin='md',
                            color='#666666'
                        ),
                        TextComponent(
                            text=activity.description,
                            size='sm',
                            wrap=True,
                            margin='md',
                            color='#666666'
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='????????????',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
                                    size='sm',
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='????????????',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.end_at.strftime("%Y/%m/%d %H:%M"),
                                    size='sm',
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='??????',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=''.join(
                                        [
                                            str(activity.session_count),
                                            '/',
                                            str(activity.session_limit)
                                        ]
                                    ),
                                    size='sm',
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='??????',
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.address,
                                    size='sm',
                                    wrap=True,
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        BoxComponent(
                            layout='horizontal',
                            spacing='sm',
                            contents=[
                                ButtonComponent(
                                    style='link',
                                    height='sm',
                                    action=PostbackAction(
                                        label='??????',
                                        data=','.join(
                                            [
                                                'join_group_activity',
                                                str(activity.id)
                                            ]
                                        )
                                    ),
                                ),
                                SeparatorComponent(

                                ),
                                ButtonComponent(
                                    style='link',
                                    height='sm',
                                    action=PostbackAction(
                                        label='??????',
                                        data=','.join(
                                            [
                                                'leave_group_activity',
                                                str(activity.id)
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(
                                label='????????????',
                                uri=''.join(
                                    [
                                        'https://www.google.com/maps/search/?api=1&query=',
                                        str(activity.lat),
                                        ',',
                                        str(activity.lng)
                                    ]
                                )
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(
                                label='????????????',
                                uri=''.join(
                                    [
                                        app.config['WHO_JOIN_ACTIVITY_LIFF_URL'],
                                        '?activity_id=',
                                        str(activity.id)
                                    ]
                                )
                            )
                        )
                    ]
                )
            )
            carousel_template_columns.append(bubble_template)
    bubble_template = BubbleContainer(
        hero=ImageComponent(
            url='https://i.imgur.com/Gtj8dTV.jpg',
            size='full',
            aspect_ratio='5:4',
            aspect_mode='cover'
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='????????????',
                        uri=''.join(
                            [
                                app.config['ADD_GROUP_ACTIVITY_LIFF_URL'],
                                '?',
                                'source_id=',
                                urllib.parse.quote_plus(str(source_id))
                            ]
                        )
                    ),
                ),
            ]
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


def join_group_activity_message(activity_id, line_user_id):
    # Query user
    user = User.query.filter_by(
        line_user_id=str(line_user_id),
        deleted_at=None
    ).first()
    # Check user us exist
    if user:
        # Query model activity
        activity = GroupActivity.query.filter_by(
            id=activity_id
        ).first()

        # Get user profile from LINE
        try:
            user_profile = line_bot_api.get_profile(line_user_id)
            user_dict = json.loads(str(user_profile))
        except:
            bubble_template = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='????????????',
                            weight='bold',
                            color='#1DB446',
                            size='md',
                        ),
                        TextComponent(
                            text='????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
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
            message = FlexSendMessage(
                alt_text='????????????', contents=bubble_template)
            return message
        if activity.deleted_at is not None:
            message = TextSendMessage(
                text=''.join([
                    user_dict['displayName'],
                    ' ??????????????? ',
                    activity.title,
                    ' ???????????????????????????????????????'
                ])
            )
            return message

        # Check now time is can join activity
        if check_time_can_join(activity.start_at):
            # Check activity session limit can join
            if activity.session_limit > activity.session_count:

                # Query activity log
                activity_log = GroupActivityLog.query.filter_by(
                    group_activity_id=str(activity_id),
                    user_id=user.id,
                    deleted_at=None
                ).first()

                if activity_log is None:
                    activity_log = GroupActivityLog(
                        group_activity_id=activity_id,
                        user_id=user.id
                    )

                    # Update activity log
                    db.session.add(activity_log)
                    try:
                        activity.session_count = activity.session_count + 1
                        db.session.commit()

                        # Update activity
                        db.session.add(activity)
                        try:
                            db.session.commit()
                            content = ''.join(
                                [
                                    user_dict['displayName'],
                                    ' ?????????????????? ',
                                    activity.title,
                                    ' ??????'
                                ]
                            )
                        except:
                            pass
                    except:
                        pass
                else:
                    content = ''.join(
                        [
                            user_dict['displayName'],
                            ' ????????????????????? ',
                            activity.title,
                            ' ??????'
                        ]
                    )
            else:
                content = ''.join(
                    [
                        user_dict['displayName'],
                        ' ??????????????? ',
                        activity.title,
                        ' ?????????????????????????????????'
                    ]
                )
        else:
            content = ''.join(
                [
                    user_dict['displayName'],
                    ' ??????????????? ',
                    activity.title,
                    ' ?????????????????????????????????????????????'
                ]
            )
        message = TextSendMessage(
            text=content
        )
    else:
        content = bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='????????????',
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text='????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
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
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)
    return message


def leave_group_activity_message(activity_id, line_user_id):
    user = User.query.filter_by(
        line_user_id=str(line_user_id),
        deleted_at=None
    ).first()

    # Check is user or not
    if user is None:
        user = User(
            line_user_id=line_user_id
        )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            pass

    # Query model activity
    activity = GroupActivity.query.filter_by(
        id=activity_id
    ).first()

    # Get user data
    try:
        user_profile = line_bot_api.get_profile(line_user_id)
        user_dict = json.loads(str(user_profile))
    except:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='????????????',
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text='????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
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
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)
        return message

    # Query activity log
    activity_log = GroupActivityLog.query.filter_by(
        group_activity_id=str(activity_id),
        user_id=user.id,
        deleted_at=None
    ).first()

    if activity_log:
        activity_log.deleted_at = datetime.datetime.now()

        # Update activity log
        db.session.add(activity_log)
        try:
            db.session.commit()
            activity.session_count = activity.session_count - 1 - int(activity_log.companion)
            other_message = ''
            if activity.session_count == 0:
                activity.deleted_at = datetime.datetime.now()
                other_message = '?????????????????????????????????????????????????????????'

            # Update activity
            db.session.add(activity)
            try:
                db.session.commit()
                content = ''.join(
                    [
                        user_dict['displayName'],
                        ' ???????????? ',
                        activity.title,
                        other_message
                    ]
                )
            except:
                pass
        except:
            pass
    else:
        content = ''.join(
            [
                user_dict['displayName'],
                ' ????????????????????? ',
                activity.title,
                ' ???'
            ]
        )
    return TextSendMessage(
        text=content
    )


def check_time_can_join(start_at):
    now = datetime.datetime.now()
    if start_at >= now:
        return True
    return False


def search_activity_message(keyword, source_id):
    now = datetime.datetime.now()
    activitys = GroupActivity.query.filter(
        GroupActivity.title.like('%{}%'.format(keyword)),
        GroupActivity.public == 1,
        GroupActivity.deleted_at == None,
        GroupActivity.end_at > now
    ).order_by(func.random()).limit(3).all()
    carousel_template_columns = []
    if activitys:
        for activity in activitys:
            footerbox = []
            if activity.group_link != None:
                footerbox = BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(
                                label='??????????????????',
                                uri=str(activity.group_link)
                            )
                        )
                    ]
                )
            bubble_template = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text=activity.title,
                            wrap=True,
                            weight='bold',
                            size='md',
                            color='#1DB446'
                        ),
                        TextComponent(
                            text=activity.description,
                            size='sm',
                            wrap=True,
                            margin='md',
                            color='#666666'
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='????????????',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
                                    size='sm',
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='????????????',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.end_at.strftime("%Y/%m/%d %H:%M"),
                                    size='sm',
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='??????',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=''.join(
                                        [
                                            str(activity.session_count),
                                            '/',
                                            str(activity.session_limit)
                                        ]
                                    ),
                                    size='sm',
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='??????',
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.address,
                                    size='sm',
                                    wrap=True,
                                    flex=5,
                                    margin='sm',
                                    color='#333333'
                                )
                            ]
                        )
                    ]
                ),
                footer=footerbox
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
                        text='????????????',
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text=''.join(['???????????????????????? ', keyword, ' ?????????']),
                        margin='md',
                        wrap=True,
                        size='md',
                    )
                ]
            ),
        )
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)

    return message


def my_join_group_activity(line_user_id):
    now = datetime.datetime.now()
    user_id = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()

    activitys = GroupActivity.query.join(
        GroupActivityLog,
        GroupActivityLog.group_activity_id == GroupActivity.id
    ).filter(
        GroupActivityLog.user_id==user_id.id,
        GroupActivity.deleted_at==None,
        GroupActivity.end_at>now
    ).order_by(
        GroupActivity.start_at.asc()
    ).limit(10).all()

    carousel_template_columns = []
    if activitys:
        for activity in activitys:
            if activity.group_link is None:
                bubble_template = BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text=activity.title,
                                wrap=True,
                                weight='bold',
                                size='md',
                                color='#1DB446'
                            ),
                            TextComponent(
                                text=activity.description,
                                size='sm',
                                wrap=True,
                                margin='md',
                                color='#666666'
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='????????????',
                                        wrap=True,
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
                                        size='sm',
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='????????????',
                                        wrap=True,
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=activity.end_at.strftime("%Y/%m/%d %H:%M"),
                                        size='sm',
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='??????',
                                        wrap=True,
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=''.join(
                                            [
                                                str(activity.session_count),
                                                '/',
                                                str(activity.session_limit)
                                            ]
                                        ),
                                        size='sm',
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='??????',
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=activity.address,
                                        size='sm',
                                        wrap=True,
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            )
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='????????????',
                                    uri=''.join(
                                        [
                                            'https://www.google.com/maps/search/?api=1&query=',
                                            str(activity.lat),
                                            ',',
                                            str(activity.lng)
                                        ]
                                    )
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='????????????',
                                    uri=''.join(
                                        [
                                            app.config['WHO_JOIN_ACTIVITY_LIFF_URL'],
                                            '?activity_id=',
                                            str(activity.id)
                                        ]
                                    )
                                )
                            )
                        ]
                    )
                )
                carousel_template_columns.append(bubble_template)
            else:
                bubble_template = BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text=activity.title,
                                wrap=True,
                                weight='bold',
                                size='md',
                                color='#1DB446'
                            ),
                            TextComponent(
                                text=activity.description,
                                size='sm',
                                wrap=True,
                                margin='md',
                                color='#666666'
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='????????????',
                                        wrap=True,
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
                                        size='sm',
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='????????????',
                                        wrap=True,
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=activity.end_at.strftime("%Y/%m/%d %H:%M"),
                                        size='sm',
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='??????',
                                        wrap=True,
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=''.join(
                                            [
                                                str(activity.session_count),
                                                '/',
                                                str(activity.session_limit)
                                            ]
                                        ),
                                        size='sm',
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='horizontal',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='??????',
                                        flex=2,
                                        size='md',
                                        color='#666666'
                                    ),
                                    TextComponent(
                                        text=activity.address,
                                        size='sm',
                                        wrap=True,
                                        flex=5,
                                        margin='sm',
                                        color='#333333'
                                    )
                                ]
                            )
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='????????????',
                                    uri=''.join(
                                        [
                                            'https://www.google.com/maps/search/?api=1&query=',
                                            str(activity.lat),
                                            ',',
                                            str(activity.lng)
                                        ]
                                    )
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='????????????',
                                    uri=''.join(
                                        [
                                            app.config['WHO_JOIN_ACTIVITY_LIFF_URL'],
                                            '?activity_id=',
                                            str(activity.id)
                                        ]
                                    )
                                )
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='??????????????????',
                                    uri=activity.group_link
                                ),
                            ),
                        ]
                    )
                )
                carousel_template_columns.append(bubble_template)
                message = FlexSendMessage(
                    alt_text='??????????????????',
                    contents=CarouselContainer(
                        contents=carousel_template_columns
                    )
                )
            message = FlexSendMessage(
                alt_text='??????????????????',
                contents=CarouselContainer(
                    contents=carousel_template_columns
                )
            )
    else:
        bubble_template = BubbleContainer(
            hero=ImageComponent(
                url='https://i.imgur.com/fpFCI1H.jpg',
                size='full',
                aspect_ratio='5:4',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='???????????????????????????',
                        color='#1DB446',
                        size='lg',
                        weight='bold'
                    ),
                    TextComponent(
                        text='?????????????????????????????????????????????????????????????????????',
                        size='md',
                        margin='sm',
                        wrap=True
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='????????????', contents=bubble_template)
    return message


def user_leave_and_private_activity(line_user_id):
    activitys = Activity.query.filter_by(
        source_id=line_user_id,
        deleted_at=None,
        public=True
    ).all()

    for activity in activitys:
        activity.public = False
        activity.group_link = None
        db.session.add(activity)
    try:
        db.session.commit()
    except:
        pass
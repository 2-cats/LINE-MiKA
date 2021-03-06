
import re

from flask import Flask

from .. import db
from ..models import Card, Issue, User
from .map import convert_address

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def add_card(data):
    location = convert_address(data['address'])

    # Check card is public?
    public = False
    if 'public' in data:
        public = True

    user = User.query.filter_by(
        line_user_id=data['line_user_id']
    ).order_by(User.created_at.desc()).first()

    card = Card.query.filter_by(
        user_id=user.id,
        deleted_at=None
    ).order_by(Card.created_at.desc()).first()

    if card:
        messages = []
        messages.append('一個人僅限一張名片，請先至『名片管理』刪除不需要的名片後，再新增一張名片！')
        return {
            'status': 'fail',
            'messages': messages
        }
    else:
        # check card in backend
        messages = []
        if data['email']:
            if not bool(re.search(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$', data['email'])):
                messages.append('不正確的電子郵件信箱')
        if data['tel_number']:
            if not bool(re.search(r'^(\d{9,10})$', data['tel_number'])):
                messages.append('不正確的電話號碼')
        if data['phone_number']:
            if not bool(re.search(r'^(\d{9,10})$', data['phone_number'] )):
                messages.append('不正確的手機號碼')
        if data['rel_link']:
            if not bool(re.search(r'^https:\/\/([\w\-./?%&=]+)', data['rel_link'] )):
                messages.append('不正確的公司網址')
        if messages: 
            return {
                'status': 'fail',
                'messages': messages
            }
        card = Card(
                user_id=user.id,
                name=data['name'],
                nickname=data['nickname'],
                company_name=data['company_name'],
                title=data['title'],
                industry=data['industry'],
                summary=data['summary'],
                email=data['email'],
                fax_number=data['fax_number'],
                tax_number=data['tax_number'],
                rel_link=data['rel_link'],
                address=data['address'],
                lat=location[0],
                lng=location[1],
                phone_number=data['phone_number'],
                tel_number=data['tel_number'],
                public=public,
                image_path=data['image_path'],
                view_count=0,
                description=''.join(
                    [
                        data['company_name'],
                        '、',
                        data['industry'],
                        '、',
                        data['address'],
                        '、',
                        data['summary']
                    ]
                )
            )
        db.session.add(card)
        try:
            db.session.commit()
        except:
            pass
        return {
            'status': 'success',
            'message': '新增成功'
        }

def edit_card(data):
    card = Card.query.filter_by(
        id=data['id']
    ).first()
    return card

def update_card(data):
    location = convert_address(data['address'])
    # Check card is public?
    public = False
    if 'public' in data:
        public = True
    card = Card.query.filter_by(
        id=data['card_id']
    ).first()
    if card:
        card.name=data['name']
        card.nickname=data['nickname']
        card.company_name=data['company_name']
        card.title=data['title']
        card.industry=data['industry']
        card.summary=data['summary']
        card.email=data['email']
        card.fax_number=data['fax_number']
        card.tax_number=data['tax_number']
        card.address=data['address']
        card.lat=location[0]
        card.lng=location[1]
        card.phone_number=data['phone_number']
        card.tel_number=data['tel_number']
        card.public=public
        card.image_path=data['image_path']
        card.rel_link=data['rel_link']

        db.session.add(card)
        try:
            db.session.commit()
        except:
            pass
        return {
            'status': 'success',
            'message': '新增成功'
        }
    else:
         return {
            'status': 'fail',
            'message': '錯誤的名片 ID'
        }

def get_card(data):
    card = Card.query.filter_by(
        id=data['card_id'],
    ).first()

    card.view_count = card.view_count + 1
    db.session.add(card)
    try:
        db.session.commit()
    except:
        pass

    image_url = ""
    if card.image_path != '':
        image_url = ''.join([
            app.config['OCR_SCAN_CARD_RESOURCE'],
            card.image_path
        ])
    card = {
        "name": card.name,
        "anime_image_path": card.anime_path,
        "image_url": image_url
    }
    return card

def report_card_issue(data):
    user = User.query.filter_by(line_user_id=data['line_user_id']).first()
    issue = Issue(
                card_id=data['card_id'],
                user_id=user.id,
                content=data['content']
            )
    db.session.add(issue)
    try:
        db.session.commit()
    except:
        pass


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
        return {
            'status': 'fail',
            'message': '一個人僅限一張名片，請先至『名片管理』刪除不需要的名片後，再新增一張名片！'
        }
    else:
        card = Card(
                user_id=user.id,
                name=data['name'],
                nickname=data['nickname'],
                line_id=data['line_id'],
                company_name=data['company_name'],
                title=data['title'],
                industry=data['industry'],
                summary=data['summary'],
                email=data['email'],
                fax_number=data['fax_number'],
                tax_number=data['tax_number'],
                address=data['address'],
                lat=location[0],
                lng=location[1],
                phone_number=data['phone_number'],
                tel_number=data['tel_number'],
                public=public,
                image_path=data['image_path']
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
        card.line_id=data['line_id']
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
    image_url = ""
    if card.image_path is not None:
        image_url = ''.join([
            app.config['OCR_SCAN_CARD_RESOURCE'],
            card.image_path
        ])
    card = {
        "name": card.name,
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

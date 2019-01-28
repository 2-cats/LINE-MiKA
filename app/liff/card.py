
from .. import db
from ..models import Card, User, Issue
from .map import convert_address

def add_card(data):
    location = convert_address(data['address'])

    user = User.query.filter_by(line_user_id=data['line_user_id']).first()
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
            tel_number=data['tel_number']
        )
    db.session.add(card)
    try:
        db.session.commit()
    except:
        pass

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
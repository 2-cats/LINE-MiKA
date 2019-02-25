from .. import db
from ..models import Card

def get_card():
    cards = Card.query.filter_by(
        deleted_at=None,
        public=1
    ).order_by(
        Card.created_at.desc()
    ).all()
    data = []
    for card in cards:
        item = {
            "id": card.id,
            "name": card.name,
            "company_name": card.company_name,
            "view_count": card.view_count,
            "description": card.description
        }
        data.append(item)
    return data
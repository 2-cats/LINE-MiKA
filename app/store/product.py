from .. import db
from ..models import Card, Order, Product

def user_use_product(user_id, product_id):
    product = Product.query.filter_by(
        id = product_id
    ).first()

    card = Card.query.filter(
        Card.user_id==user_id,
        Card.deleted_at==None
    ).first()

    if product.product_type == "cosplay":
        card.cosplay_path = product.image_path
    elif product.product_type == "anime":
        card.cosplay_path = product.image_path

    db.session.add(card)
    try:
        db.session.commit()
    except:
        pass
    
    user = {
        "id": user_id
    }
    return user

def get_product_detail(product_id, user_id):
    product = Product.query.filter_by(
        id = product_id
    ).first()
    order = Order.query.filter_by(
        user_id = user_id,
        product_id = product_id
    ).first()
    button_text = '購買'
    if order or product.price==0:
        button_text = '使用'

    product={
        "demo_image_path": product.demo_image_path,
        "price": product.price,
        "author": product.author,
        "name": product.name,
        "button_text": button_text,
        "user_id": user_id,
        "id": product_id,
        "description": product.description
    }
    return product

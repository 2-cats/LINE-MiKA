from .. import db
from ..models import Card, Order, Product

def user_use_product(user_id, product_id):
    message = ""
    product = Product.query.filter_by(
        id = product_id
    ).first()

    card = Card.query.filter(
        Card.user_id==user_id,
        Card.deleted_at==None
    ).first()
    if card :
        if product.product_type == "cosplay":
            card.cosplay_path = product.image_path
        elif product.product_type == "anime":
            card.anime_path = product.image_path

        db.session.add(card)
        try:
            db.session.commit()
        except:
            message = '更換失敗，請重新嘗試！'
    else:
        message = '你沒有新增過名片喔！請先新增名片'
        
    datas = {
        "id": user_id
    }
    datas = {
        "messages": message,
        "user": {
            "id": user_id
        }
    }
    return datas

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

def anime_store_product(user_id):
    product_dates = []

    # Query free product.
    products = Product.query.filter_by(
        product_type="anime",
        deleted_at=None
    ).all()

    for product in products:
        item = {
            "name": product.name,
            "demo_image_path": product.demo_image_path,
            "product_id": product.id,
            "user_id": user_id
        }
        product_dates.append(item)

    user = {
        "id": user_id
    }

    return product_dates, user

def cosplay_store_product(user_id):
    product_dates = []

    # Query free product.
    products = Product.query.filter_by(
        product_type="cosplay",
        deleted_at=None
    ).all()

    for product in products:
        item = {
            "name": product.name,
            "demo_image_path": product.demo_image_path,
            "product_id": product.id,
            "user_id": user_id
        }
        product_dates.append(item)
    
    user = {
        "id": user_id
    }
    return product_dates, user
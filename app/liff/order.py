from flask import Flask
from linebot import LineBotApi

from ..models import Order, Product

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def my_order(user_id):
    order_dates = []

    # Query free product.
    products = Product.query.filter_by(
        price=0
    ).all()

    for product in products:
        item = {
            "name": product.name,
            "demo_image_path": ''.join([
                app.config['APP_URL'],
                product.demo_image_path
            ]),
            "detail_url": ''.join([
                app.config['APP_URL'],
                'line/product/detail?product_id=',
                str(product.id),
                '&user_id=',
                str(user_id)
            ])
        }
        order_dates.append(item)
    
    # Query order history.
    orders = Order.query.filter_by(
        user_id=user_id
    ).all()

    for order in orders:
        item = {
            "name": order.product.name,
            "demo_image_path": ''.join([
                app.config['APP_URL'],
                order.product.demo_image_path
            ]),
            "detail_url": ''.join([
                app.config['APP_URL'],
                'line/product/detail?product_id=',
                str(order.product.id),
                '&user_id=',
                str(user_id)
            ])
        }
        order_dates.append(item)

    return order_dates

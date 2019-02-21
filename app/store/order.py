from ..models import Order, Product


def my_order(user_id):
    order_dates = []

    # Query free product.
    products = Product.query.filter_by(
        price=0
    ).all()

    for product in products:
        item = {
            "name": product.name,
            "demo_image_path": product.demo_image_path,
            "product_id": product.id,
            "user_id": user_id
        }
        order_dates.append(item)
    
    # Query order history.
    orders = Order.query.filter_by(
        user_id=user_id
    ).all()

    for order in orders:
        item = {
            "name": order.product.name,
            "demo_image_path": order.product.demo_image_path,
            "product_id": order.product.id,
            "user_id": user_id
        }
        order_dates.append(item)

    user = {
        "id": user_id
    }
    return order_dates, user

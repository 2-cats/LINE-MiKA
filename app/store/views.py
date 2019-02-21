from flask import Flask, abort, current_app, render_template, request

from . import store
from .. import db
from .order import my_order
from .product import get_product_detail, user_use_product
@store.route("/line/store", methods=['GET'])
def index():
    if request.method == 'GET':
        data = request.args.to_dict()
        orders = my_order(data['user_id'])
        return render_template(
            'line/store/my_order.html',
            orders=orders
        )

@store.route("/line/product/detail", methods=['GET'])
def product_detail():
    if request.method == 'GET':
        data = request.args.to_dict()
        product = get_product_detail(data['product_id'],data['user_id'])
        return render_template(
            'line/product/detail.html',
            product=product
        )

@store.route("/line/product/use", methods=['GET'])
def use_product():
    if request.method == 'GET':
        data = request.args.to_dict()
        user = user_use_product(data['user_id'], data['product_id'])
        return render_template(
            'line/product/use.html',
            user=user
        )


from flask import Flask, abort, current_app, render_template, request

from . import store
from .. import db
from .order import my_order
from .product import (anime_store_product, cosplay_store_product, get_product_detail,
                      user_use_product)


@store.route("/line/store", methods=['GET'])
def order_index():
    if request.method == 'GET':
        data = request.args.to_dict()
        datas = my_order(data['user_id'])
        return render_template(
            'line/store/order.html',
            orders=datas[0],
            user=datas[1],
        )

@store.route("/line/store/anime", methods=['GET'])
def anime_store_index():
    if request.method == 'GET':
        data = request.args.to_dict()
        data = anime_store_product(data['user_id'])
        return render_template(
            'line/store/anime.html',
            products=data[0],
            user=data[1]
        )

@store.route("/line/store/cosplay", methods=['GET'])
def cosplay_store_index():
    if request.method == 'GET':
        data = request.args.to_dict()
        data = cosplay_store_product(data['user_id'])
        return render_template(
            'line/store/cosplay.html',
            products=data[0],
            user=data[1]
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

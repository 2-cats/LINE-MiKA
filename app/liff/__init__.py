from flask import Blueprint

liff = Blueprint('liff', __name__)
from . import views
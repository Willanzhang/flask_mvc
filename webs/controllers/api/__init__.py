# coding = utf-8
from flask import Blueprint

route_api = Blueprint('api_page', __name__)
from webs.controllers.api.Member import *

@route_api.route("/")
def index():
    return "Mina Api v1.0~"


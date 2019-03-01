from webs.controllers.index import route_index
from application import app

app.register_blueprint(route_index, url_prefix="/")

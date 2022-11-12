from flask import Blueprint
from flask_restx import Api

from .views import YoaView, Login, Register

api_blueprint = Blueprint("api", __name__, url_prefix="/kntl/kuda/v1")

api = Api(
    api_blueprint,
    version="1.0",
    tittle="Your Assistance",
    description="Assistance will remind you"
)

api.add_resource(YoaView, '/yoa')
api.add_resource(Login, "/login-kntl")
api.add_resource(Register, "/register-kntl")
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
mi = Migrate()
lm = LoginManager()
cors = CORS()
jwt = JWTManager()
from flask import Flask

from .ext import db, ma, mi, lm, cors, jwt

DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'kntl kntl'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = "kntl-kntl"  
    db.init_app(app)
    mi.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    from .models import User
    from core.api.routes import api_blueprint

    app.register_blueprint(api_blueprint)

    lm.login_view = "auth.login"
    lm.init_app(app)

    @lm.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


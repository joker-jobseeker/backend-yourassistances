from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256

from .ext import db

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Integer, default=0)
    yourassistance = db.relationship('YourAssistance')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

   # method
    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True
    
    @staticmethod
    def generate_hash(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return  pbkdf2_sha256.verify(password, hash)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def __repr__(self):
        return f'<User {self.username}>'

class YourAssistance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

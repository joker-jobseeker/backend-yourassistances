from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256

from .ext import db

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(300),nullable=False )
    is_admin = db.Column(db.Integer, default=0)
    yourassistance = db.relationship('YourAssistance', backref="yourassistance", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self._password = generate_password_hash(password)

    def check_password(self, _password):
        pbkdf2_sha256.hash(_password)

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True
    
    @staticmethod
    def generate_hash(_password):
        return pbkdf2_sha256.hash(_password)

    @staticmethod
    def verify_hash(_password, hash):
        return  pbkdf2_sha256.verify(_password, hash)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def __repr__(self):
        return f'<User {self.username}>'

class YourAssistance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    data = db.Column(db.String(20000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

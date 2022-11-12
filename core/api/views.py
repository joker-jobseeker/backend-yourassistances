from flask_restx import Resource, reqparse
from flask import jsonify, abort, make_response
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from flask_login import login_user

from core.api.schema import yoa_schemas
from core.models import YourAssistance, User
from core.ext import db


class Register(Resource):
    def post(self):
        register_parser = reqparse.RequestParser()
        register_parser.add_argument(
            'email', location='json', type=str, required=True
        )
        register_parser.add_argument(
            'userName', location='json', type=str, required=True
        )
        register_parser.add_argument(
            'passwordHash', location='json', type=str, required=True 
        )

        args = register_parser.parse_args()
        email = args["email"]
        userName = args['userName']
        passwordHash = args['passwordHash']
        passwordHash = User.__init__(passwordHash)
        
        if email == "" or userName == "" or passwordHash == "":
            return jsonify({"message": "incorrect Username or Password"})

        # save to database
        try:
            new_user = User(email=email, username=userName, password=passwordHash)
            db.session.add(new_user)
            db.session.commit()

            #creating access token
            access_token = create_access_token(identify=userName)
        except:
            return abort(400, f'Email {email}, is already exist')
        return jsonify(
            {
                "message": "User Created successfully",
                "token": access_token
            }
        )


class Login(Resource):
    def post(self):
        login_parser = reqparse.RequestParser()
        login_parser.add_argument("email", location="json", type=str, required=True)
        login_parser.add_argument("password", location="json", type=str, required=True)

        args = login_parser.parse_args()
        email = args["email"]
        password = args["password"]

        if email == "" or password == "":
            return jsonify({"message": "No file selected"}), 401

        email = email.lower()
        current_user = User.__init__(email)
        if not current_user:
            return jsonify({"message": "User Not Found"}), 401

        if User.check_password(password, current_user.password):
            current_user.authenticated = True
            access_token = create_access_token(identity=email)

            # save to database
            db.session.add(current_user)
            db.session.commit()
            login_user(current_user)
            response = jsonify(
                {
                    "identity": current_user.email,
                    "token": access_token
                }
            )

            # set access token in cookie
            set_access_cookies(response, access_token)
            return response
        else:
            make_response(
                "could not verify",
                402,
                {"www-Authenticate": 'Basic realm="Login Required"'}
            )


class Logout(Resource):
    def post(self):
        response = make_response(jsonify({"message": "Logged out"}))

        # unsetting access token in cooke
        unset_jwt_cookies(response)
        return response
            

class YoaView(Resource):
    
    def get(self):
        assistances = YourAssistance.query.all()
        jwt_required(assistances)
        return yoa_schemas.dump(assistances)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', action='append')
        parser.add_argument('paragraph', action='append')
        jwt_required(parser)
        return jsonify(
            {
                "message": "Your Assistance will remind you"
            }
        )
from flask_restx import Resource, reqparse
from flask import jsonify, abort, make_response
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from flask_login import login_user
from sqlalchemy.exc import IntegrityError

from core.api.schema import yoa_schemas
from core.models import YourAssistance, Users
from core.ext import db

class Register(Resource):
    def post(self):
        register_parser = reqparse.RequestParser()
        register_parser.add_argument(
            "username", location="json", type=str, required=True
        )
        register_parser.add_argument(
            "email", location="json", type=str, required=True)
        register_parser.add_argument(
            "password", location="json", type=str, required=True
        )

        args = register_parser.parse_args()
        username = args["username"]
        email = args["email"]
        password = args["password"]
        password = Users.generate_hash(password)
        
        if username == "" or email == "" or password == "":
            return jsonify({"message": "Incorrect Username or Password"}), 400

        # save to database
        try:
            new_user = Users(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            # creating acess token
            access_token = create_access_token(identity=username)

        except IntegrityError:
            return abort(400, f"User {username} is Already Exist")

        return jsonify(
            {
                "message": "User created successfully",
                "token": access_token,
            }
        )


class Login(Resource):
    def post(self):
        login_parser = reqparse.RequestParser()
        login_parser.add_argument(
            "username", location="json", type=str, required=True)
        login_parser.add_argument(
            "password", location="json", type=str, required=True)

        args = login_parser.parse_args()
        
        email = args["email"]
        password = args["password"]


        if email == "" or password == "":
            return jsonify({"message": "No file selected"}), 401

        email = email.lower()
        current_user = Users.find_by_email(email)
        if not current_user:
            return jsonify({"message": "User not found"}), 400

        if Users.verify_hash(password, current_user.password):
            access_token = create_access_token(identity=email)

            # save to database
            db.session.add(current_user)
            db.session.commit()
            login_user(current_user)
            response = jsonify(
                {
                    "identity": current_user.username,
                    "token": access_token,
                }
            )

            # set access token in cookie
            set_access_cookies(response, access_token)
            return response

        else:
            make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
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
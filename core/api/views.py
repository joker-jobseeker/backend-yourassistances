from flask_restx import Resource, reqparse
from flask import jsonify, abort, make_response, request
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from flask_login import login_user, current_user
from sqlalchemy.exc import IntegrityError
import json

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
            "email", location="json", type=str, required=True
        )
        register_parser.add_argument(
            "password", location="json", type=str, required=True
        )

        args = register_parser.parse_args()
        username = args["username"]
        email = args["email"]
        password = args["password"]

        # passwordhash = Users.generate_hash(password)

        # kondisi kalo kosong semua
        # if username == "" or email == "" or password == "":
        #     return abort(400, "username, email, or password doesn't fill")

        # # buat kondisi  password
        # elif password == "":
        #     return abort(400, "Password can't be empty")
        # elif len(password) <= 6:
        #     return abort(400, "password must more than 6 character")

        # if email == "":
        #     return abort(400, "Username can't be empty")
        # elif username == "":
        #     return abort(400, "Username can't be empty")

        # save to database
        try:
            new_user = Users(username=username, email=email, password=Users.generate_hash(password))
            db.session.add(new_user)
            db.session.commit()
            print("aman")

        except IntegrityError:
            db.session.rollback()


        return jsonify(
            {
                "message": "User created successfully", 
            }
        )


class Login(Resource):
    def post(self):
        login_parser = reqparse.RequestParser()
        login_parser.add_argument(
            "email", location="json", type=str, required=True)
        login_parser.add_argument(
            "password", location="json", type=str, required=True)

        args = login_parser.parse_args()

        email = args['email']

        password = args["password"]

        if email == "" or password == "":
            return jsonify({"message": "No file selected"}), 401

        email = email.lower()
        current_user = Users.find_by_email(email=email)
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
                    "token": access_token
                }
            )

            # set access token in cookie
            set_access_cookies(response, access_token)
            # raise Exception(response)
            return response

        else:
            return make_response(
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
    # @jwt_required()
    def get(self):
        assistances = YourAssistance.query.all()
        return yoa_schemas.dump(assistances)

     # task untuk wira
    def post(self):
        title = request.form.get('title')
        data = request.form.get('data')
        if len(title) < 3:
            return abort(400, "your title is too short")
        if len(data) < 50:
            return abort(400, "your paragraph is too short")
        new_post = YourAssistance(title=title, data=data)
        db.session.add(new_post)
        db.session.commit()
        return jsonify(
            {
                "message": "Your Assistance will remind you"
            }
        )

    # task untuk wira

    def put(self):
        # note = YourAssistance.query.get(id)
        # n

        pass

    def delete(self):
        note = json.loads(request.data)
        noteId = note['noteId']
        note = YourAssistance.query.get(noteId)
        if note:
            if note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()

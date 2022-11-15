from flask_restx import Resource, reqparse
from flask import jsonify, abort, make_response, request
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, get_jwt_identity
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
    @jwt_required()
    def get(self):
        assistances = YourAssistance.query.all()
        result = []
        email = get_jwt_identity()
        current_user = Users.find_by_email(email=email)
        for assistance in assistances:
            dict_res = {}
            dict_res["id"] = assistance.id
            dict_res["title"] = assistance.title
            dict_res["data"] = assistance.data
            dict_res["date"] = assistance.date
            dict_res["user_id"] = assistance.person_id
            result.append(dict_res)
        return make_response(jsonify({"message":result, "email":email}), 200)

    @jwt_required()
    def post(self):
        title = request.get_json(force=True)['title']
        data = request.get_json(force=True)['data']

        email = get_jwt_identity()
        current_user = Users.find_by_email(email=email)

        new_post = YourAssistance(title=title, data=data, person_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return make_response(jsonify(
            {
                "value": title,
                "status": "crot",
            }
        ), 200)

    @jwt_required()
    def put(self):
        
        id = int(request.get_json(force=True)['id'])
        message = []
        email = get_jwt_identity()
        current_user = Users.find_by_email(email=email)
        try:
            todo = YourAssistance.query.get(id)
            if current_user.id == todo.person_id:
                try:
                    new_title = request.get_json(force=True)['title']
                    todo.title = new_title
                    db.session.commit()
                    message.append("Edit title success")
                except:
                    pass
                try:
                    new_data = request.get_json(force=True)['data']
                    todo.data =  new_data
                    db.session.commit()
                    message.append("Edit data success")
                except:
                    pass
                
                return make_response(jsonify({"message":message}), 200)
            else:
                return make_response(jsonify({"message": "You are not eligible to edit this post"}), 401)
        except:
            return make_response(jsonify({"message": "can't find post."}), 401)
        
    @jwt_required()
    def delete(self):
        id = int(request.get_json(force=True)['id'])
        email = get_jwt_identity()
        current_user = Users.find_by_email(email=email)
        try:
            todo = YourAssistance.query.get(id)
            if current_user.id == todo.person_id:
                db.session.delete(todo)
                db.session.commit()
                return make_response(jsonify({"message":"delete success."}), 200)
            else:
                return make_response(jsonify({"message": "You are not eligible to edit this post."}), 401)
        except:
            return make_response(jsonify({"message": "can't find post."}), 401)
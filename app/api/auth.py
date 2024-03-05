from flask_restx import Resource, Namespace, marshal, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, Unauthorized

from app.services import users as users_service

api = Namespace("auth")

credentials_model = api.model(
    "CredentialsModel", {"username": fields.String, "password": fields.String}
)

user_model = api.model("UserModel", {"id": fields.Integer, "username": fields.String})

auth_model = api.model(
    "AuthModel",
    {
        "user": fields.Nested(user_model),
        "access_token": fields.String,
    },
)


@api.route("/")
class Login(Resource):

    @api.expect(credentials_model)
    @api.response(200, "Success", auth_model)
    def post(self):
        user = users_service.find_user_by_username(api.payload.get("username"))

        if not user:
            raise Unauthorized("Invalid credentials. Please try again")

        if not check_password_hash(user.password, api.payload.get("password")):
            raise Unauthorized("Invalid credentials. Please try again")

        return {
            "user": marshal(user, user_model),
            "access_token": create_access_token(identity=user.id),
        }, 200


@api.route("/registration")
class Registration(Resource):

    @api.expect(credentials_model)
    @api.response(201, "Created", auth_model)
    def post(self):
        user = users_service.find_user_by_username(api.payload["username"])

        if user:
            raise BadRequest(
                "User with the provided username has been already registered"
            )

        new_user = users_service.create_user(
            username=api.payload.get("username"),
            password=generate_password_hash(api.payload.get("password")),
        )

        return {
            "user": marshal(new_user, user_model),
            "access_token": create_access_token(identity=new_user.id),
        }, 201

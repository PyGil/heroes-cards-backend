from flask_restx import Api

from app.api.auth import api as auth_api
from app.api.heroes_cards import api as heroes_cards_api

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(authorizations=authorizations)

api.add_namespace(auth_api, path="/auth")
api.add_namespace(heroes_cards_api, path="/heroes-cards")

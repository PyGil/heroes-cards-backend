from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest, NotFound

from app.api.auth import user_model
from app.services import heroes_cards as cards_service

api = Namespace("heroes-cards")


card_model = api.model(
    "CardModel",
    {
        "id": fields.Integer,
        "time_created": fields.Date,
        "time_updated": fields.Date,
        "name": fields.String,
        "skill_description": fields.String,
        "skill_damage": fields.String,
        "health": fields.Integer,
        "creator": fields.Nested(user_model),
    },
)

create_card_model = api.model(
    "CreateCardModel",
    {
        "name": fields.String(required=True),
        "skill_description": fields.String(required=True),
        "skill_damage": fields.String(required=True),
        "health": fields.Integer(required=True),
    },
)


update_card_model = api.model(
    "UpdateCardModel",
    {
        "name": fields.String,
        "skill_description": fields.String,
        "skill_damage": fields.String,
        "health": fields.Integer,
    },
)


@api.route("/")
class HeroCards(Resource):

    @jwt_required()
    @api.doc(security="jsonWebToken")
    @api.expect(create_card_model)
    @api.marshal_with(card_model)
    def post(self):
        card = cards_service.find_card_by_name(api.payload.get("name"))

        if card:
            raise BadRequest("Card with the provided name has been already created")

        return cards_service.create_card(
            name=api.payload.get("name"),
            skill_description=api.payload.get("skill_description"),
            skill_damage=api.payload.get("skill_damage"),
            health=api.payload.get("health"),
            creator_id=get_jwt_identity(),
        )

    @api.marshal_list_with(card_model)
    def get(self):
        return cards_service.find_all_cards()


@api.route("/<int:card_id>")
class HeroCard(Resource):

    @api.marshal_with(card_model)
    def get(self, card_id: int):
        card = cards_service.find_card_by_id(card_id)

        if not card:
            raise NotFound("Card does not exist")

        return card

    @jwt_required()
    @api.doc(security="jsonWebToken")
    @api.expect(update_card_model)
    @api.marshal_with(card_model)
    def patch(self, card_id: int):
        card = cards_service.find_card_by_id(card_id)

        if not card:
            raise NotFound("Card does not exist")

        return cards_service.update_card(
            card,
            name=api.payload.get("name"),
            skill_description=api.payload.get("skill_description"),
            skill_damage=api.payload.get("skill_damage"),
            health=api.payload.get("health"),
        )

    @jwt_required()
    @api.doc(security="jsonWebToken")
    def delete(self, card_id: int):
        card = cards_service.find_card_by_id(card_id)

        if not card:
            raise NotFound("Card does not exist")

        cards_service.remove_card(card)


@api.route("/my-cards")
class UsersHeroCards(Resource):

    @jwt_required()
    @api.doc(security="jsonWebToken")
    @api.marshal_list_with(card_model)
    def get(self):
        return cards_service.find_all_cards_by_creator_id(get_jwt_identity())

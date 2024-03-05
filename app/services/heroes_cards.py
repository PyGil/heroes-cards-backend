from typing import Union, Dict, List

from app.extensions import db
from app.models.hero_card import HeroCard


def create_card(
    name: str,
    skill_description: str,
    skill_damage: int,
    health: int,
    creator_id: int,
    execute_commit=True,
) -> HeroCard:
    card = HeroCard(
        name=name,
        skill_description=skill_description,
        skill_damage=skill_damage,
        health=health,
        creator_id=creator_id,
    )

    db.session.add(card)

    if execute_commit:
        db.session.commit()

    return card


def find_card_by_name(name: str) -> Union[HeroCard, None]:
    return HeroCard.query.filter_by(name=name).first()


def find_card_by_id(id: int) -> Union[HeroCard, None]:
    return HeroCard.query.get(id)


def find_all_cards() -> List[HeroCard]:
    return HeroCard.query.all()


def find_all_cards_by_creator_id(creator_id: id) -> Union[HeroCard, None]:
    return HeroCard.query.filter_by(creator_id=creator_id).all()


def update_card(
    card: HeroCard,
    execute_commit=True,
    **card_dto: Dict[str, Union[str, int]],
) -> HeroCard:

    for key, value in card_dto.items():
        if value and hasattr(card, key):
            setattr(card, key, value)

    if execute_commit:
        db.session.commit()

    return card


def remove_card(
    card: HeroCard,
    execute_commit=True,
) -> None:
    db.session.delete(card)

    if execute_commit:
        db.session.commit()

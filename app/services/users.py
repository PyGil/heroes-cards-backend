from typing import Union

from app.extensions import db
from app.models.user import User


def create_user(username: str, password: str, execute_commit=True) -> User:
    user = User(username=username, password=password)

    db.session.add(user)

    if execute_commit:
        db.session.commit()

    return user


def find_user_by_username(username: str) -> Union[User, None]:
    return User.query.filter_by(username=username).first()

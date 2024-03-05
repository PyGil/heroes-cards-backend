from app.extensions import db


class HeroCard(db.Model):
    __tablename__ = "heroes_cards"

    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    name = db.Column(db.String(50), unique=True, nullable=False)
    skill_description = db.Column(db.String(150), nullable=False)
    skill_damage = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)

    creator_id = db.Column(db.ForeignKey("users.id"))
    creator = db.relationship("User", back_populates="created_carts")

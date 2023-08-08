from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    bookings = db.relationship("Booking", back_populates="user")

    @classmethod
    def authenticate(cls, **kwargs):
        user_name = kwargs.get("user_name")
        password = kwargs.get("password")
        if (not user_name) or (not password):
            return None

        user = cls.query.filter_by(user_name=user_name).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            user_name=self.user_name,
            is_admin=self.is_admin,
        )


class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(200), nullable=False)

    shows = db.relationship("ShowSchedule", backref="theatre", lazy=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            address=self.address,
            capacity=self.capacity,
            image_name=self.image_name,
        )


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(300))
    image_name = db.Column(db.String(200), nullable=False)

    show_schedules = db.relationship("ShowSchedule", back_populates="show", lazy=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            rating=self.rating,
            tags=self.tags,
            image_name=self.image_name,
        )


class ShowSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey("theatre.id"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    show_time = db.Column(db.DateTime, nullable=False)

    show = db.relationship("Show", back_populates="show_schedules")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey("theatre.id"), nullable=False)
    show_schedule_id = db.Column(
        db.Integer, db.ForeignKey("show_schedule.id"), nullable=False
    )

    user = db.relationship("User", back_populates="bookings")
    show = db.relationship("Show")
    theatre = db.relationship("Theatre")
    show_schedule = db.relationship("ShowSchedule")

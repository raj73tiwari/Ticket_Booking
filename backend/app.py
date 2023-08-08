import os
import base64
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    verify_jwt_in_request,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
    current_user,
)
from functools import wraps
from flask_caching import Cache
from worker import celery_init_app
import tasks
from celery.result import AsyncResult
from celery.schedules import crontab

from models import User, Theatre, Show, ShowSchedule, Booking,db

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Th_Booking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "Book_It by Sahastranshu"
jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=2)
app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"



migrate = Migrate(app, db)
cache = Cache(app)


celery_app = celery_init_app(app)


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Models................................


db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        new_user = User(
            email="admin@gmail.com",
            user_name="admin",
            password=generate_password_hash("admin"),
            is_admin=True,
        )
        db.session.add(new_user)
        db.session.commit()


# current user ...............................


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Admin.......................................


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Restricted-Admins only!"}), 403

        return decorator

    return wrapper


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    print(data)
    user = User.query.filter_by(email=data["email"]).first()
    user2 = User.query.filter_by(user_name=data["user_name"]).first()
    if user or user2:
        return jsonify({"message": "Email or UserName already exists!"}), 422
    new_user = User(
        email=data["email"],
        user_name=data["user_name"],
        password=generate_password_hash(data["password"]),
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Signed Up Successfully."}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)
    user = User.authenticate(**data)
    if not user:
        return jsonify({"message": "Invalid credentials !"}), 403
    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(
        identity=user.id, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(identity=user.id)
    print(user.to_dict())
    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict(),
            }
        ),
        201,
    )


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "logged out successfully !"})
    unset_jwt_cookies(response)
    return response


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_tkn():
    id = current_user.id
    additional_claims = {"is_admin": current_user.is_admin}
    access = create_access_token(identity=id, additional_claims=additional_claims)
    print("access token refreshed")
    return (
        jsonify(
            {
                "access_token": access,
            }
        ),
        200,
    )


@app.route("/user", methods=["GET"])
@admin_required()
def users():
    users = User.query.order_by(User.id.desc()).all()
    print(users)
    t_users = []
    for u in users:
        t_users.append(u.to_dict())
    return jsonify(t_users), 200


@app.route("/theatre", methods=["GET"])
@cache.cached(timeout=60, key_prefix="theatre")
def theatre():
    theatres = Theatre.query.order_by(Theatre.id.desc()).all()
    t_serial = []
    for t in theatres:
        t_serial.append(t.to_dict())
    return jsonify(t_serial), 200


@app.route("/createTheatre", methods=["POST"])
@admin_required()
def createTheatre():
    data = request.get_json()
    thea = Theatre.query.filter_by(name=data["name"]).first()
    if thea:
        return jsonify({"message": "Theatre already exists !"}), 422
    if data["img"] and data["name"] and data["seat"] and data["address"]:
        image_data = data["img"].split(",")[1]
        filename = secure_filename(f"th_{data['name'].replace(' ', '_')}.jpg")
        file_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        new_theatre = Theatre(
            name=data["name"],
            image_name=filename,
            capacity=data["seat"],
            address=data["address"],
        )
        db.session.add(new_theatre)
        db.session.commit()
        cache.delete("theatre")
        return (
            jsonify({"message": "Data received and theatre created successfully !"}),
            201,
        )
    return jsonify({"message": "Please provide necessary data fields !"}), 406


@app.route("/uploads/<filename>")
def serve_photo(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/getTheatre/<int:id>", methods=["GET"])
def getTheatre(id):
    theatre = Theatre.query.filter_by(id=id).first()
    if not theatre:
        return jsonify({"meassage": "Theatre not found"}), 404
    return jsonify(theatre.to_dict()), 200


@app.route("/deleteTheatre/<int:id>", methods=["POST"])
@admin_required()
def deleteTheatre(id):
    theatre = Theatre.query.filter_by(id=id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404
    if theatre.image_name:
        file_path = os.path.join(
            app.root_path, app.config["UPLOAD_FOLDER"], theatre.image_name
        )
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(theatre)
    db.session.commit()
    cache.delete("theatre")
    return jsonify({"message": "Theatre deleted successfully"}), 200


@app.route("/updateTheatre/<int:id>", methods=["POST"])
@admin_required()
def update_theatre(id):
    theatre = Theatre.query.filter_by(id=id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404
    data = request.get_json()
    if not data["name"] or not data["seat"] or not data["address"]:
        return jsonify({"message": "Please provide necessary data fields !"}), 406
    thea = Theatre.query.filter_by(name=data["name"]).first()
    if thea and thea.id != id:
        return jsonify({"message": "Theatre already exists !"}), 422

    if data["img"]:
        if theatre.image_name:
            file_path = os.path.join(
                app.root_path, app.config["UPLOAD_FOLDER"], theatre.image_name
            )
            if os.path.exists(file_path):
                os.remove(file_path)

        image_data = data["img"].split(",")[1]
        filename = secure_filename(f"th_{data['name'].replace(' ', '_')}.jpg")
        file_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        theatre.image_name = filename

    theatre.name = data["name"]
    theatre.address = data["address"]
    theatre.capacity = data["seat"]

    db.session.commit()
    cache.delete("theatre")

    return jsonify({"message": "Theatre updated successfully"}), 200


@app.route("/show", methods=["GET"])
@cache.cached(timeout=60, key_prefix="show")
def show():
    shows = Show.query.order_by(Show.id.desc()).all()
    t_show = []
    for s in shows:
        t_show.append(s.to_dict())
    return jsonify(t_show), 200


@app.route("/createShow", methods=["POST"])
@admin_required()
def createShow():
    data = request.get_json()
    show = Show.query.filter_by(name=data["name"]).first()
    if show:
        return jsonify({"message": "Show already exists !"}), 422
    if data["img"] and data["name"] and data["tags"] and data["rating"]:
        image_data = data["img"].split(",")[1]
        filename = secure_filename(f"sh_{data['name'].replace(' ', '_')}.jpg")
        file_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        new_show = Show(
            name=data["name"],
            image_name=filename,
            rating=data["rating"],
            tags=data["tags"],
        )
        db.session.add(new_show)
        db.session.commit()
        cache.delete("show")
        return (
            jsonify({"message": "Data received and show created successfully !"}),
            201,
        )
    return jsonify({"message": "Please provide necessary data fields !"}), 406


@app.route("/deleteShow/<int:id>", methods=["POST"])
@admin_required()
def deleteShow(id):
    show = Show.query.filter_by(id=id).first()
    if not show:
        return jsonify({"message": "Show not found !"}), 404
    if show.image_name:
        file_path = os.path.join(
            app.root_path, app.config["UPLOAD_FOLDER"], show.image_name
        )
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(show)
    db.session.commit()
    cache.delete("show")
    return jsonify({"message": "Show deleted successfully !"}), 200


@app.route("/updateShow/<int:id>", methods=["POST"])
@admin_required()
def update_show(id):
    show = Show.query.filter_by(id=id).first()
    if not show:
        return jsonify({"message": "Show not found"}), 404
    data = request.get_json()
    if not data["name"] or not data["rating"] or not data["tags"]:
        return jsonify({"message": "Please provide necessary data fields !"}), 406
    sho = Show.query.filter_by(name=data["name"]).first()
    if sho and sho.id != id:
        return jsonify({"message": "Show already exists !"}), 422

    if data["img"]:
        if show.image_name:
            file_path = os.path.join(
                app.root_path, app.config["UPLOAD_FOLDER"], show.image_name
            )
            if os.path.exists(file_path):
                os.remove(file_path)

        image_data = data["img"].split(",")[1]
        filename = secure_filename(f"sh_{data['name'].replace(' ', '_')}.jpg")
        file_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        show.image_name = filename

    show.name = data["name"]
    show.rating = data["rating"]
    show.tags = data["tags"]

    db.session.commit()
    cache.delete("show")

    return jsonify({"message": "Show updated successfully"}), 200


@app.route("/addShow/<int:theatre_id>", methods=["POST"])
@admin_required()
def addShow(theatre_id):
    data = request.get_json()
    if not data["show_id"] or not data["price"] or not data["time"]:
        return jsonify({"message": "Please provide necessary data fields !"}), 406

    theatre = Theatre.query.filter_by(id=theatre_id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404

    show = Show.query.filter_by(id=data["show_id"]).first()
    if not show:
        return jsonify({"message": "Show not found"}), 404

    show_schedule = ShowSchedule(
        theatre_id=theatre_id,
        show_id=data["show_id"],
        price=data["price"],
        show_time=datetime.strptime(data["time"], "%Y-%m-%dT%H:%M"),
    )
    db.session.add(show_schedule)
    db.session.commit()
    return jsonify({"message": "Show added to the theatre successfully"}), 201


@app.route("/getShows/<int:theatre_id>", methods=["GET"])
def getTheatreShows(theatre_id):
    print(theatre_id, 878749824)
    theatre = Theatre.query.filter_by(id=theatre_id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404
    shows = theatre.shows
    shows_list = []
    for show_schedule in shows:
        show_data = {
            'schedule_id':show_schedule.id,
            "id": show_schedule.show.id,
            "name": show_schedule.show.name,
            "rating": show_schedule.show.rating,
            "tags": show_schedule.show.tags,
            "image_name": show_schedule.show.image_name,
            "price": show_schedule.price,
            "time": show_schedule.show_time.isoformat(),
        }
        shows_list.append(show_data)
    shows_list.reverse()

    return jsonify(shows_list), 200


@app.route("/removeShow/<int:theatre_id>/<int:show_id>", methods=["POST"])
@admin_required()
def removeShow(theatre_id, show_id):
    theatre = Theatre.query.filter_by(id=theatre_id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404

    show = Show.query.filter_by(id=show_id).first()

    if not show:
        return jsonify({"message": "Show not found"}), 404

    show_schedule = ShowSchedule.query.filter_by(
        theatre_id=theatre_id, show_id=show_id
    ).first()

    if not show_schedule:
        return jsonify({"message": "Show is not scheduled "}), 404

    db.session.delete(show_schedule)
    db.session.commit()

    return jsonify({"message": "Show removed from the theatre successfully"}), 200


@app.route("/theatre/<int:theatre_id>/show/<int:show_id>/schedule/<int:schedule_id>/seats", methods=["GET"])
def getSeats(theatre_id, show_id,schedule_id):
    theatre = Theatre.query.filter_by(id=theatre_id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404

    show = Show.query.filter_by(id=show_id).first()
    if not show:
        return jsonify({"message": "Show not found"}), 404

    show_schedule = ShowSchedule.query.filter_by(
       id=schedule_id
    ).first()
    if not show_schedule:
        return jsonify({"message": "Show is not scheduled in this theatre"}), 404

    total_seats = theatre.capacity

    booked_seats_count = Booking.query.filter_by(
       show_schedule_id=show_schedule.id
    ).count()

    empty_seats = total_seats - booked_seats_count

    return jsonify(empty_seats), 200


@app.route("/bookShow/<int:theatre_id>", methods=["POST"])
@jwt_required()
def bookShow(theatre_id):
    data = request.get_json()
    show_id = data.get("show_id")
    schedule_id = data.get("schedule_id")
    user_id = data.get("user_id")

    theatre = Theatre.query.filter_by(id=theatre_id).first()
    if not theatre:
        return jsonify({"message": "Theatre not found"}), 404

    show = Show.query.filter_by(id=show_id).first()
    if not show:
        return jsonify({"message": "Show not found"}), 404

    show_schedule = ShowSchedule.query.filter_by(id=schedule_id).first()
    if not show_schedule:
        return jsonify({"message": "Show is not scheduled !"}), 404

    booked_seats_count = Booking.query.filter_by(
        show_schedule_id=show_schedule.id
    ).count()
    if booked_seats_count >= theatre.capacity:
        return jsonify({"message": "Housefull. Cannot book more seats."}), 400

    booking = Booking(
        user_id=user_id,
        theatre_id=theatre_id,
        show_id=show_id,
        show_schedule_id=show_schedule.id,
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Show Booked Successfully"}), 201


@app.route("/bookings/<int:user_id>", methods=["GET"])
@jwt_required()
def userBookings(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    bookings_data = []
    bookings = user.bookings
    for booking in bookings:
        booking_data = {
            "id": booking.id,
            "theatre_name": booking.theatre.name,
            "show_id": booking.show_id,
            "show_name": booking.show.name,
            "show_tags": booking.show.tags,
            "show_rating": booking.show.rating,
            "show_price": booking.show_schedule.price,
            "show_image": booking.show.image_name,
            "show_time": booking.show_schedule.show_time.isoformat(),
        }
        print(booking_data)
        bookings_data.append(booking_data)

    return jsonify(bookings_data), 200




# .................Backend Jobs......................


@app.post("/export/<id>")
@admin_required()
def export(id) -> dict[str, object]:
    theatre = Theatre.query.filter_by(id=id).first()
    shows = theatre.shows
    shows_list = []
    for show_schedule in shows:
        show_data = {
            "id": show_schedule.show.id,
            "name": show_schedule.show.name,
            "rating": show_schedule.show.rating,
            "tags": show_schedule.show.tags,
            "image_name": show_schedule.show.image_name,
            "price": show_schedule.price,
            "time": show_schedule.show_time.isoformat(),
        }
        shows_list.append(show_data)
    shows_list.reverse()
    result = tasks.generate_theatre_csv.delay(theatre.to_dict(), shows_list)
    return {"result_id": result.id}


@app.get("/export_result/<id>")
@admin_required()
def export_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }


@app.route("/get_exported_files", methods=["GET"])
@admin_required()
def get_exported_files():
    exports_folder = "exports"
    exported_files = []
    if os.path.exists(exports_folder):
        exported_files = os.listdir(exports_folder)
    return jsonify(exported_files)


@app.route("/download/<filename>", methods=["GET"])
@admin_required()
def download_file(filename):
    exports_folder = "exports"
    file_path = os.path.join(exports_folder, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404
    




# ....................Scheduled Jobs........................


@celery_app.on_after_configure.connect
def setup_daily_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18),
        tasks.send_reminder_emails.s(),   
    )


@celery_app.on_after_configure.connect
def setup_monthly_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=5, day_of_month='L'),
        tasks.send_entertainment_report.s(),   
    )







# ~/go/bin/MailHog
# celery -A app:celery_app worker -l INFO
# celery -A app:celery_app beat -l INFO





if __name__ == "__main__":
    app.run(debug=True)

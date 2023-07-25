import os
import base64
from flask import Flask,request,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt,verify_jwt_in_request, \
                               unset_jwt_cookies, jwt_required, JWTManager,current_user
from functools import wraps
from flask_caching import Cache









app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Th_Booking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "Book_It by Sahastranshu"
jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=2)



db = SQLAlchemy(app)
migrate = Migrate(app, db)


 
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






# Models................................






class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(120),unique=True,nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean(),default=False)
    shows_booked = db.relationship('Shows', back_populates='booked_by')

    @classmethod
    def authenticate(cls, **kwargs):
        user_name = kwargs.get('user_name')
        password = kwargs.get('password')
        if (not user_name) or (not password):
            return None

        user = cls.query.filter_by(user_name=user_name).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user
    
    def to_dict(self):
        return dict(id=self.id, email=self.email, user_name=self.user_name,is_admin=self.is_admin,shows=self.shows_booked)
    


class Theatre(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120),unique=True,nullable=False)
    address=db.Column(db.String(200),nullable=False)
    capacity=db.Column(db.Integer,nullable=False)
    image_name=db.Column(db.String(200), nullable=False)
    shows = db.relationship('Shows', back_populates='theatre')

    def to_dict(self):
        return dict(id=self.id, name=self.name, address=self.address,capacity=self.capacity,image_name=self.image_name)
    
    
class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(200))
    ticket_price = db.Column(db.Float, nullable=False)

    
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    theatre = db.relationship('Theatre', back_populates='shows')

    
    booked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booked_by = db.relationship('User', back_populates='shows_booked')

    def to_dict(self):
        return dict(id=self.id, name=self.name, rating=self.rating,tags=self.tags,ticket_price=self.ticket_price)





with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@gmail.com').first():
        new_user=User(email="admin@gmail.com",user_name="admin",password=generate_password_hash("admin"),is_admin=True)  
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
                return jsonify({'message':"Restricted-Admins only!"}), 403

        return decorator

    return wrapper




@app.route("/signup",methods=['POST'])
def signup():
    data = request.get_json()
    print(data)
    user=User.query.filter_by(email=data['email']).first()
    user2=User.query.filter_by(user_name=data['user_name']).first()
    if user or user2:
            return jsonify({'message':"Email or UserName already exists!"}),422
    new_user=User(email=data['email'],user_name=data['user_name'],password=generate_password_hash(data['password']))  
    db.session.add(new_user)
    db.session.commit()    
    return jsonify({'message':"Signed Up Successfully."}),201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    user = User.authenticate(**data)
    if not user:
        return jsonify({ 'message': 'Invalid credentials !'}),403
    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(identity=user.id,additional_claims=additional_claims)
    refresh_token=create_refresh_token(identity=user.id)
    print(user.to_dict())
    return jsonify({'access_token':access_token,'refresh_token':refresh_token,'user':user.to_dict()}),201


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "logged out successfully !"})
    unset_jwt_cookies(response)
    return response


@app.route('/refresh',methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_tkn():
    id=current_user.id
    additional_claims = {"is_admin": current_user.is_admin}
    access=create_access_token(identity=id,additional_claims=additional_claims)
    print('access token refreshed')
    return jsonify({
        'access_token':access,
    }),200


@app.route('/user',methods=['GET'])
@jwt_required()
def my_profile():
   return jsonify(current_user.to_dict())


@app.route('/check',methods=['GET'])
@admin_required()
def check():
    return jsonify({"isAdmin":current_user.is_admin})



@app.route('/theatre',methods=['GET'])
@jwt_required()
def theatre():
    theatres = Theatre.query.order_by(Theatre.id.desc()).all()
    t_serial=[]
    for t in theatres:
        t_serial.append(t.to_dict())
    return jsonify(t_serial)


@app.route('/createTheatre', methods=['POST'])
@admin_required()
def createTheatre():
        data = request.get_json()
        thea=Theatre.query.filter_by(name=data['name']).first()
        if thea:
            return jsonify({'message':"Theatre already exists !"}),422
        if data['img'] and data['name'] and data['seat'] and data['address']:
            image_data = data['img'].split(',')[1]
            filename = secure_filename(f"th_{data['name'].replace(' ', '_')}.jpg")
            file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(image_data))
            
            new_theatre=Theatre(name=data['name'],image_name=filename,capacity=data['seat'],address=data['address'])
            db.session.add(new_theatre)
            db.session.commit()
            return jsonify({'message': 'Data received and theatre created successfully !'}),201
        return jsonify({'message':'Please provide necessary data fields !'}),406

@app.route('/uploads/<filename>')
def serve_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/getTheatre/<int:id>', methods=['GET'])
def getTheatre(id):
    theatre = Theatre.query.filter_by(id=id).first()
    if not theatre:
        return jsonify({'meassage': 'Theatre not found'}), 404
    return jsonify(theatre.to_dict()),200


@app.route('/deleteTheatre/<int:id>', methods=['POST'])
@admin_required()
def deleteTheatre(id):
    theatre = Theatre.query.filter_by(id=id).first()
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404
    if theatre.image_name:
        file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], theatre.image_name)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(theatre)
    db.session.commit()
    return jsonify({'message': 'Theatre deleted successfully'}), 200


@app.route('/updateTheatre/<int:id>', methods=['POST'])
@admin_required()
def update_theatre(id):
    theatre = Theatre.query.filter_by(id=id).first()
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404
    data = request.get_json()
    if not data['img'] or not data['name'] or not data['seat'] or not data['address']:
        return jsonify({'message':'Please provide necessary data fields !'}),406
    thea=Theatre.query.filter_by(name=data['name']).first()
    if thea and thea.id!=id:
        return jsonify({'message':"Theatre already exists !"}),422
    if theatre.image_name:
        file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], theatre.image_name)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    image_data = data['img'].split(',')[1]
    filename = secure_filename(f"th_{data['name'].replace(' ', '_')}.jpg")
    file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(image_data))
    theatre.image_name = filename
    theatre.name = data['name']
    theatre.address = data['address']
    theatre.capacity = data['seat']

    db.session.commit()

    return jsonify({'message': 'Theatre updated successfully'}), 200


    
















@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



if __name__ == "__main__":
    app.run(debug=True)

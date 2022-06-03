'''
Author: James Thomason
Date: 6/3/2022
'''
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from psycopg2 import IntegrityError
import bcrypt
from werkzeug.utils import secure_filename
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/ReceiKeep'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
db = SQLAlchemy(app)
CORS(app)
app.config["JWT_SECRET_KEY"] = ""  # Change this!
jwt = JWTManager(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Event: {self.description}'

    def __init__(self, description):
        self.description = description

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable = False)
    user_images = db.relationship("Image", backref='user')
    

    def __repr__(self):
        return f'User: {self.username}'

    def __init__(self,username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


#  end of models
# ------------------------------------------------------------------------------
# Start of routes
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token":access_token, "identity":identity["username"]}, 200

@app.route("/register", methods=["POST"])
def register():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        
        check_user = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()
        if check_user:
            return "User already exists", 400
        if check_email:
            return "Email already in use.", 400
        if not username:
            return "Missing Username", 400
        if not password:
            return "Missing password", 400
        if not email:
            return "Missing email", 400
        
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(username=username, password=hashed_pass.decode('utf-8'),email=email)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity={"username":username})
        refresh_token = create_refresh_token(identity={"username": username})
        return {"access_token":access_token, "refresh_token":refresh_token}, 200


    except IntegrityError:
        db.session.rollback()
        return 'User already exists', 400
    except AttributeError:
        return "Please provide an email and password in JSON in the request body", 400

@app.route("/login", methods=["POST"])
def login():
    
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return "Username Required", 400
    if not password:
        return "Password Required", 400
        
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found", 404
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity={"username": user.username})
        refresh_token = create_refresh_token(identity={"username": user.username})
        return {"access_token": access_token, "refresh_token":refresh_token}, 200
    else:
        return "Invalid Login Info, Please try again.", 400

@app.route("/images", methods=["GET"])
@jwt_required()
def allImages():
    '''
    current_user = get_jwt_identity()
    if request.method == "GET":
        images = Image.query.order_by(Image.created_at.asc()).all()
        image_list = [format_image(x) for x in images]
        return {"images": image_list}
    '''
    pass

@app.route("/image/<int:id>", methods=["GET","DELETE"])
@jwt_required()
def images_Id():
    '''
    if request.method == GET:
        do stuff
    if request.method == DELETE:
        delete image
    '''
    pass

# Testing image uploading.
@app.route("/imageUpload", methods=["POST"])
def uploadImages():
    pic = request.files['pic']

    if not pic:
        return "No picture uploaded/found", 400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Image(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return "Image has been uploaded", 200

@app.route("/images/<int:id>", methods=["GET"])
def getImages():
    img = Image.query.filter_by(id=id)
    if not img:
        return "Image not found with id", 404
    return Response(data=img.img, mimetype=img.mimetype)

# End testing image upload

if __name__ == "__main__":
    app.run(debug=True)

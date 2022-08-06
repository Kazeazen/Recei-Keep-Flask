'''
Author: James Thomason
Date: 6/3/2022
'''
import os
from flask import Flask, request
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
import secrets_for_backend

UPLOAD_FOLDER = 'Uploads/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + secrets_for_backend.POSTGRES_PASS + '@localhost/ReceiKeep'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
CORS(app)
app.config["JWT_SECRET_KEY"] = secrets_for_backend.POSTGRES_SECRET_KEY  # Change this!
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable = False)
    images = db.relationship("Image", backref='user')
    
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
    img = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    mimetype = db.Column(db.String, nullable=False)


#  end of models
# ------------------------------------------------------------------------------

def format_image(image):
    return {
        "id":image.id,
        "img": image.img,
        "name": image.name,
        "mimetype": image.mimetype,
        "created_at": image.created_at
    }

# Start of routes
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token":access_token, "identity":identity["username"]}, 200

# Creating a new user
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

        access_token = create_access_token(identity={"username":username,"email": email})
        refresh_token = create_refresh_token(identity={"username": username, "email":email})
        return {"access_token":access_token, "refresh_token":refresh_token}, 200


    except IntegrityError:
        db.session.rollback()
        return 'User already exists', 400
    except AttributeError:
        return "Please provide a valid username and password in the JSON request body", 400

# Logging in 
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
        access_token = create_access_token(identity={"username": user.username, "email": user.email})
        refresh_token = create_refresh_token(identity={"username": user.username, "email": user.email})
        return {"access_token": access_token, "refresh_token":refresh_token}, 200
    else:
        return "Invalid Login Info, Please try again.", 400

# Getting all images or uploading a new one
@app.route("/images", methods=["GET", "POST"])
@jwt_required()
def allImages():
    current_user = get_jwt_identity()
    if request.method == "GET":
        user = User.query.filter_by(username=current_user["username"]).first()
        images = Image.query.filter_by(parent_id = user.id)
        image_list = [format_image(x) for x in images]
        return {"images": image_list}
    if request.method == "POST":
        current_user = get_jwt_identity()
        pic = request.files.get('file', None)
        if not pic:
            return "No picture uploaded/found", 400
        user = User.query.filter_by(username=current_user["username"]).first()
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pic.save(path)
        img = Image(img=path, mimetype=mimetype, name=filename, parent_id = user.id)
        # Might have to worry about duplicate images, but I personally dont see 
        # it as an issue unless duplicate id's pop up somehow
        db.session.add(img)
        db.session.commit()
    return "Image has been uploaded", 200

# Getting a specific image, deleting a specific image, or updating the image info
@app.route("/images/<string:id>", methods=["GET", "DELETE", "PUT"])
@jwt_required()
def getImages(id):
    current_user = get_jwt_identity()
    image_id = int(id)
    if not image_id:
        return "Image not found with given ID, please try again.", 404
    
    if request.method == "GET":
        user = User.query.filter_by(username=current_user["username"]).first()
        img = Image.query.filter_by(id=image_id, parent_id = user.id).first()
        if not img or user.id != img.parent_id: # Second half is to ensure other users cant delete/access people's image entry in db's
            return "Image not found with id, or wrong user is currently logged in.", 404
        return format_image(img), 200

    if request.method =="DELETE":
        user = User.query.filter_by(username=current_user["username"]).first()
        img = Image.query.filter_by(id=image_id, parent_id = user.id).first()
        if not img or user.id != img.parent_id:
            return "Image not found with id, or wrong user is currently logged in.", 404
        db.session.delete(img)
        os.remove(app.config['UPLOAD_FOLDER'] + img.name)
        db.session.commit()
        # Remove the picture from the uploads folder
        return "Success", 200

    if request.method == "PUT":
        user = User.query.filter_by(username=current_user["username"]).first()
        img = Image.query.filter_by(id=image_id, parent_id = user.id).first()
        new_name = request.json.get("name", None)
        if not new_name:
            return "Improper data sent over, only accepts name in JSON", 404
        if not img or user.id != img.parent_id:
            return "Image not found with id, or wrong user is currently logged in.", 404
        img.name = new_name
        db.session.commit()
        return f'Image {img.id} has been updated.'

if __name__ == "__main__":
    app.run(debug=True)

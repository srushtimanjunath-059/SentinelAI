from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sentinel.db"
app.config["SECRET_KEY"] = "sentinel_secret_key"


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)



class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(200))



class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Integer)

    location = db.Column(db.String(50))

    device = db.Column(db.String(50))

    risk_score = db.Column(db.Integer)

    result = db.Column(db.String(100))



with app.app_context():

    db.create_all()



@app.route("/")
def home():

    return jsonify({
        "message":"Sentinel AI Backend Running",
        "status":"Active"
    })



@app.route("/register", methods=["POST"])
def register():

    data=request.json

    hashed=bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")


    user=User(
        username=data["username"],
        password=hashed
    )


    db.session.add(user)

    db.session.commit()


    return jsonify({
        "message":"User created"
    })



@app.route("/login", methods=["POST"])
def login():

    data=request.json


    user=User.query.filter_by(
        username=data["username"]
    ).first()


    if user and bcrypt.check_password_hash(
        user.password,
        data["password"]
    ):

        return jsonify({
            "message":"Login successful",
            "status":"authorized"
        })


    return jsonify({
        "message":"Invalid login"
    }),401



if __name__=="__main__":

    app.run(debug=True)
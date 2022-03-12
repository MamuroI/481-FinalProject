import os

from flask import Flask,jsonify, request, render_template,make_response
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')  # Change this!
jwt = JWTManager(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
@cross_origin()
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Wrong username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(user=username,access_token=access_token)


@app.route("/hello", methods=["GET"])
@cross_origin()
@jwt_required()
def hello():
    response = {
        "message": "hello world"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)


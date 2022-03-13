import os
from flask import Flask,jsonify, request, render_template,make_response
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL, MySQLdb

from main import testbackend, searchTitle, searchIngredient, listFav

app = Flask(__name__)
CORS(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')  # Change this!
jwt = JWTManager(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '481final'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
@cross_origin()
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = (%s) AND password = (%s)", (username,password))
    dataSelect = cur.fetchall()
    mysql.connection.commit()
    print(dataSelect)
    if not dataSelect:
        return jsonify({"msg": "Wrong username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(user=username, access_token=access_token)

@app.route("/register", methods=["POST"])
@cross_origin()
def create_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    print(username,email,password)
    print(type(username))
    print(type(email))
    print(type(password))
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username,password,email) VALUES (%s,%s,%s)", (username, password, email))
    mysql.connection.commit()
    response = {
        "message": "register success"
    }
    return jsonify(response)


@app.route("/hello", methods=["GET"])
@cross_origin()
@jwt_required()
def hello():
    username = get_jwt_identity()
    response = {
        "message": "hello world"
    }
    return jsonify(response)

@app.route("/test", methods=["POST"])
@cross_origin()
# @jwt_required()
def test():
    # username = get_jwt_identity()
    data = request.get_json()['testvar']
    print(data)
    result = testbackend(data)
    return jsonify(result)

@app.route("/searchTitle", methods=["POST"])
@cross_origin()
@jwt_required()
def searchTit():
    data = request.get_json()['query']
    result = searchTitle(data)
    # print(result)
    return jsonify(result)

@app.route("/searchIngredient", methods=["POST"])
@cross_origin()
@jwt_required()
def searchIng():
    data = request.get_json()['query']
    result = searchIngredient(data)
    # print(result)
    return jsonify(result)

@app.route("/getFav", methods=["GET"])
@cross_origin()
@jwt_required()
def getFav():
    user = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("SELECT recipe_id FROM favourite WHERE username = (%s)", [user])
    dataSelect = cur.fetchall()
    mysql.connection.commit()
    result = listFav(dataSelect)
    return jsonify(result)

@app.route("/addFav", methods=["POST"])
@cross_origin()
@jwt_required()
def addFav():
    user = get_jwt_identity()
    recipeIndex = request.get_json()['recipeIndex']
    cur = mysql.connection.cursor()
    cur.execute("SELECT recipe_id FROM favourite WHERE username = (%s)", [user])
    dataSelect = cur.fetchall()
    mysql.connection.commit()
    print(type(dataSelect))
    if recipeIndex in str(dataSelect):
        response = {
            "message": "this recipe is already favourite"
        }
        return jsonify(response)
    else:
        cur.execute("INSERT INTO favourite (username,recipe_id) VALUES (%s,%s)", (user, recipeIndex))
    mysql.connection.commit()
    response = {
        "message": "add favourite success"
    }
    return jsonify(response)

@app.route("/removeFav", methods=["POST"])
@cross_origin()
@jwt_required()
def removeFav():
    user = get_jwt_identity()
    recipeIndex = request.get_json()['recipeIndex']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM favourite WHERE username = (%s) AND recipe_id = (%s)", (user, recipeIndex))
    mysql.connection.commit()
    response = {
        "message": "remove favourite success"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)


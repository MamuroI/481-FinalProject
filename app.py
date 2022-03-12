from flask import Flask,jsonify, request, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class RecipeSearch(Resource):
    def get(self):
        return {"data":"testing result"}

    def post(self):
        query = request.json['query']
        score = request.json['score']
        return "query:" + query + " score: " + score

api.add_resource(RecipeSearch,"/song")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


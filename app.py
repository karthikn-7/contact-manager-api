from flask import Flask
from flask import jsonify
from pymongo import Mongoclient
app = Flask(__name__)


@app.get("/api/contacts")
def contacts():
    return jsonify(message = {
        "message":"all contacts",
    })


@app.post("/api/contacts")
def contacts():
    pass



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5002)
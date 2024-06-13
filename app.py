from flask import Flask, request, jsonify
from config.dbconnection import dbconnection

app = Flask(__name__)
valid_fields = ["name","email", "phone"]

@app.route("/contacts", methods=["GET"])
def contacts():
    client = dbconnection()
    db = client["myContacts-backend"]
    collection = db["contacts"]
    try:
        return list(collection.find({}, {"_id": False}))
    except Exception as err:
        print(err)


@app.route("/contacts", methods=["POST"])
def postcontacts():
    contact_doc = request.get_json()
    for k, v in contact_doc.items():
        if k not in valid_fields and len(v) == 0:
            return jsonify({
                "description":"valid field: name, email, phone",
                "message": f"Invalid field '{k}'",
                }),400
        if not v:
            return jsonify({
                "description":"valid field: name, email, phone",
                "message": "every fields are mandatory",
                }),400
    
    try:
        client = dbconnection()
        db = client["myContacts-backend"]
        collection = db["contacts"]
        contact = collection.insert_one(contact_doc)
        inserted_id = str(contact.inserted_id)
        response = ({
            "message":"contact created",
            "_id":inserted_id
            })
        return jsonify(response),201
    except Exception as ex:
        return jsonify({
            "message": "Failed to create contact",
            "error": str(ex)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)

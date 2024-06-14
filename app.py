from flask import Flask, request, jsonify, json
from config.dbconnection import dbconnection
from bson import ObjectId, json_util
from middleware.valid_fields import field_validate, update_field_validate

app = Flask(__name__)


client = dbconnection()
db = client["myContacts-backend"]
collection = db["contacts"]

# for bson to json 
def parse_json(data):
    return json.loads(json_util.dumps(data))

# get all contacts
# GET /contacts
@app.route("/contacts", methods=["GET"])
def contacts():
    try:
        contact = collection.find()
        contact = parse_json(contact)
        return contact
    except Exception as err:
        return jsonify({'error_message':err})


# create contacts
# POST /contacts
@app.route("/contacts", methods=["POST"])
def postcontacts():
    contact_doc = request.get_json()
    response = field_validate(contact_doc)
    if response:
        return response
    try:
        # Insert the document into the collection
        contact = collection.insert_one(contact_doc)
        inserted_id = str(contact.inserted_id)
        response = {
            "message": "Contact created",
            "_id": inserted_id
        }
        return jsonify(response), 201
    except Exception as ex:
        return jsonify({
            "message": "Failed to create contact",
            "error": str(ex)
        }), 500

# get contact by id
# GET contact/<id>
@app.route("/contacts/<id>", methods=["get"])
def get_contact(id):
    try:
        id = ObjectId(id)
        contact = collection.find_one({'_id':id})
        contact = parse_json(contact)
        return contact
    except Exception as ex:
        return jsonify({'error':'Not found', 'error_message':f'{ex}'})


# delete contact by id
# DELETE contact/<id>
@app.route("/contacts/<id>", methods=["DELETE"])
def delete_contact(id):
    try:
        id = ObjectId(id)
        contact = collection.find_one_and_delete({'_id':id})
        if contact:
            contact = parse_json(contact)
            return jsonify({'message':'contact deleted', 'deleted contact':f'{contact}'}),200
        else:
            return jsonify({'message':'contact not found'}),404
    except Exception as ex:
        return jsonify({'error':'Not found', 'error_message':f'{ex}'})

# update contact
# PUT contacts/<id>
@app.route("/contacts/<id>",methods=["PUT"])
def update_contact(id):
    # object id error handling
    try:
        id = ObjectId(id)
    except Exception as err:
        return jsonify({'error':f'{err}'})
    
    try:
        updated_cont = request.get_json()
        response = update_field_validate(updated_cont)
        if response:
            return response
        else:
            try:
                res = collection.find_one_and_update({'_id':id},{'$set':updated_cont})
                return jsonify({'message':'contact updated','updated_contact':f'{res}'})
            except Exception as err:
                return jsonify({'error':f'{err}'})
    except Exception as err:
        return jsonify({'error':f'{err}'})



# error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found',"error_message":f'{error}'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed',"error_message":f'{error}'}), 405

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'error': 'Unsupported media type', 'error_message':f'{error}'}), 415

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error', 'error_message':f'{error}'}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)

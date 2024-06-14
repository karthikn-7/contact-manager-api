from flask import jsonify

def field_validate(doc:dict):
    valid_fields = ["name","email", "phone"]
    for k in doc.keys():
        if k not in valid_fields:
            return jsonify({
                "description": "Valid fields: name, email, phone",
                "message": f"Invalid field '{k}'"
            }), 400
    for v in doc.values():
        if not v:
            return jsonify({
                "description": "Valid fields: name, email, phone",
                "message": "Every field is mandatory"
            }), 400
        
    for field in valid_fields:
        if field not in doc:
            return jsonify({
                "description": "Valid fields: name, email, phone",
                "message": f"Missing field '{field}'"
            }), 400
    
    return None


def update_field_validate(doc:dict):

    valid_fields = ["name","email", "phone"]
    if len(doc.keys()) < 1:
        return jsonify({
                "description": "Atleast one field required to update",
                "message": f"No of fields: {len(doc.keys())}"
            }), 400
    for k in doc.keys():
        if k not in valid_fields:
            return jsonify({
                "description": "Valid fields: name, email, phone",
                "message": f"Invalid field '{k}'"
            }), 400
    for v in doc.values():
        if not v:
            return jsonify({
                "description": "Valid fields: name, email, phone",
                "message": "Every field is mandatory"
            }), 400
    
    return None
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import *
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

@app.route("/")
def index():
    return "Hello"


## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks(jwt):
    print(jwt)
    try:
        drinks = Drink.query.all()
        print(drinks)
    except:
        abort(422)
    drinks_formatted = [drink.short() for drink in drinks]
    if len(drinks_formatted) != 0:
        return jsonify({
            "success": True,
            "drinks": drinks_formatted
        })
    abort(404)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail", methods=["GET"])
def get_detailed_drinks():
    try:
        drinks = Drink.query.all()
    except:
        abort(422)
    drinks_formatted = [drink.long() for drink in drinks]
    if len(drinks_formatted) != 0:
        return jsonify({
            "success": True,
            "drinks": drinks_formatted
        })
    abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
def make_drink():
    details = query.get_json()
    try:
        drink = Drink(title=details["title"], recipe=details["recipe"])
        db.session.add(drink)
        db.commit()
    except:
        abort(422)
    return jsonify({
            "success": True,
            "drinks": drink.long()
    })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:id>", methods=["PATCH"])
def get_id_drink(id):
    try:
        drink = None
        drink = Drink.query.filter_by(id=id).first()
    except:
        abort(422)
    if drink:
        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    abort(404)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:id>", methods=["PATCH"])
def delete_drink(id):
    try:
        drink = None
        drink = Drink.query.filter_by(id=id).first()
        Drink.query.filter_by(id=id).first().delete()
        db.session.commit()
    except:
        abort(422)
    if drink:
        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    abort(404)


## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'forbidden'
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource Not Found"
                    }), 404

@app.errorhandler(AuthError)
def error_auth(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

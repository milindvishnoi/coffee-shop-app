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
uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


@app.route("/")
def index():
    return "Hello"


# ROUTES
@app.route("/drinks", methods=["GET"])
def get_drinks():
    try:
        drinks = Drink.query.all()
    except BaseException:
        abort(422)
    drinks_formatted = [drink.short() for drink in drinks]
    print(drinks_formatted)
    if len(drinks_formatted) != 0:
        return jsonify({
            "success": True,
            "drinks": drinks_formatted
        })
    abort(404)


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_detailed_drinks(jwt):
    try:
        drinks = Drink.query.all()
    except BaseException:
        abort(422)
    drinks_formatted = [drink.long() for drink in drinks]
    if len(drinks_formatted) != 0:
        return jsonify({
            "success": True,
            "drinks": drinks_formatted
        })
    abort(404)


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def make_drink(jwt):
    details = request.get_json()
    print(details)
    try:
        drink = Drink(title=details["title"], recipe=details["recipe"])
        drink.insert()
    except BaseException:
        abort(422)
    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def get_id_drink(jwt, id):
    details = request.get_json()
    new_title = details.get('title', None)
    new_recipe = details.get('recipe', None)
    print(new_title)

    try:
        drink = None
        drink = Drink.query.filter_by(id=id).first()
        if new_title is not None:
            drink.title = new_title
        if new_recipe is not None:
            drink.recipe = new_recipe
        drink.update()
    except BaseException:
        abort(422)
    if drink:
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    abort(404)


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(jwt, id):
    try:
        drink = None
        drink = Drink.query.filter_by(id=id).first()
        Drink.query.filter_by(id=id).first().delete()
        db.session.commit()
    except BaseException:
        abort(422)
    if drink:
        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    abort(404)


# Error Handling
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

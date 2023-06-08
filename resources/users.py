import models

from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'user')

@users.route("/", methods=["GET"])
def get_all_users():
    try:
        users = [model_to_dict(users) for users in models.User.select()]
        print(users)
        return jsonify(data = users, status={"code": 200, "message": "Success"})
    except:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# Route for registering/creating the user
@users.route("/register", methods=["POST"])
def register():
    payload = request.get_json()

    payload["email"] = payload["email"].lower()
    payload["username"] = payload["username"].lower()\
    
    try:
        models.User.get(models.User.email == payload["email"])

        return jsonify(
            data = {},
            message = "A user with that email already exists",
            status = 401
        ), 401
    except models.DoesNotExist:
        pw_hash = generate_password_hash(payload["password"])

        created_user = models.User.create(
            username = payload["username"],
            email = payload["email"],
            password = pw_hash            
        )


        created_user_dict = model_to_dict(created_user)

        print(created_user_dict)
        
        created_user_dict.pop("password")

        return jsonify(
            data = created_user_dict,
            message = f"Registered user: {created_user_dict['email']}",
            status = 201
        ), 201

# Find/Show
@users.route('/<id>', methods=["GET"])
def get_user(id):
    user = models.User.get_by_id(id)
    print(user.__dict__)

    return jsonify(
        data = model_to_dict(user),
        status = 200,
        message = "success"
    ), 200


# Update
@users.route("/<id>", methods=["PUT"])
def update_user(id):
    payload = request.get_json()
    query = models.User.update(**payload).where(models.User.id == id)
    query.execute()
    response = model_to_dict(models.User.get_by_id(id))
    return jsonify(
        data = response,
        status = 200,
        message = "User updated"
    ), 200


# Delete
@users.route("/<id>", methods=["DELETE"])
def delete_user(id):
    query = models.User.delete().where(models.User.id == id)
    test = models.Character.delete().where(models.Character.owner == id)
    query.execute()
    test.execute()
    return jsonify(
        data = "User deleted",
        message = "User deleted",
        status = 200,
    ), 200
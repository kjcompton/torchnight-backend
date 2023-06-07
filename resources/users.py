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

# Route for registering the user
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

        login_user(created_user)

        created_user_dict = model_to_dict(created_user)

        print(created_user_dict)
        
        created_user_dict.pop("password")

        return jsonify(
            data = created_user_dict,
            message = f"Registered user: {created_user_dict['email']}",
            status = 201
        ), 201


@users.route("/login", methods=["POST"])
def login():
    payload = request.get_json()
    payload["email"] = payload["email"].lower()
    payload["username"] = payload["username"].lower()

    try:
        user = models.User.get(models.User.email == payload["email"])

        # if the user exists
        user_dict = model_to_dict(user)

        # set password boolean value
        password_is_good = check_password_hash(user_dict["password"], payload["password"])

        # check if password is correct
        if (password_is_good):
            # Log the user in using flask_login
            login_user(user)
            print(f"{current_user.username}: this is current_user.username in the POST login")

            return jsonify(
                data = user_dict,
                message = f"{user_dict['email']} has successfully logged in!",
                status = 200
            ), 200
        else:
            print("Password is incorrect")
            return jsonify(
                data = {},
                message = "The email and/or password is incorrect",
                status = 401
            ), 401
    except models.DoesNotExist:

        # if the user does not exist
        print("Email is not found")

        return jsonify(
                data = {},
                message = "The email and/or password is incorrect",
                status = 401
            ), 401

# Create
@users.route("/", methods=["POST"])
def create_users():
    payload = request.get_json()
    new_user = models.User.create(**payload)
    print(payload)
    return jsonify(payload)


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
    query = models.User.update(**payload).where(models.Dog.id == id)
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
    query.execute()
    return jsonify(
        data = "User deleted",
        message = "User deleted",
        status = 200,
    ), 200
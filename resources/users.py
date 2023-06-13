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
    payload["username"] = payload["username"].lower()
    
    try:
        models.User.get(models.User.email == payload["email"])

        return jsonify(
            data = {},
            message = "A user with that email already exists",
            status = 401
        ), 401
    except models.DoesNotExist:
        # pw_hash = generate_password_hash(payload["password"])
        pw_hash = payload["password"]

        created_user = models.User.create(
            username = payload["username"],
            email = payload["email"],
            password = pw_hash,
            gold = payload["gold"]      
        )


        created_user_dict = model_to_dict(created_user)

        print(created_user_dict)
        
        created_user_dict.pop("password")

        return jsonify(
            data = created_user_dict,
            message = f"Registered user: {created_user_dict['email']}",
            status = 201
        ), 201
    
# Log In
@users.route("/login", methods=["GET"])
def login():
    print(request.url)
    print(request.args.get('email'))
    print(request.args.get('password'))
    email = request.args.get('email').lower()
    password = request.args.get('password')
    try:
        models.User.get(models.User.email == email)
        print("Found email")
        found_user = models.User.get(models.User.email == email)
        newUser = model_to_dict(found_user)
        if newUser["password"] == password:
            print("Passwords Match")
            return jsonify(
                data = newUser,
                message = "password match",
                status = 201
            ), 201
        else:
            print("Passwords DONT Match")
            return jsonify(
                data = "password no match",
                message = "password no match",
                status = 201
            ), 201
        # print(found_user["email"])
        # print(found_user["password"])
        # print(payload["password"])

        # return jsonify(
        #     data = "User found",
        #     message = "User found",
        #     status = 201
        # ), 201
    except models.DoesNotExist:
        print("Did not find")
        return jsonify(
            data = 'User doesnt exist',
            message = 'User doesnt exist',
            status = 201
        ), 201

    # try:
    #     models.User.get(models.User.email == payload["email"])
    #     user = models.User.get(models.User.email == payload["email"])
    #     print()
    #     return jsonify(
    #         data = user,
    #         message = "A user with that email already exists",
    #         status = 401
    #     ), 401
    # except:
        

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
    # Finds the user and deletes them and their related characters
    user = models.User.get(models.User.id == id)
    user.delete_instance(recursive=True)
    return jsonify(
        data = "User deleted",
        message = "User deleted",
        status = 200,
    ), 200
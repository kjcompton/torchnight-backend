import models

from flask import Blueprint, jsonify, request

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
        message = "User deleted"
        status = 200,
    ), 200
import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

characters = Blueprint('characters', 'character')

@characters.route("/", methods=["GET"])
def get_all_characters():
    try:
        characters = [model_to_dict(characters) for characters in models.Character.select()]
        print(characters)
        return jsonify(data = characters, status={"code": 200, "message": "Success"})
    except:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# Create
@characters.route("/", methods=["POST"])
def create_character():
    payload = request.get_json()
    print(payload)
    new_character = models.Character.create(**payload)
    print(new_character)

    character_dict = model_to_dict(new_character)


    
    return jsonify(
        data = character_dict,
        message = "Character successfully created!",
        status = 201
    ), 201


# Find/Show
@characters.route('/<id>', methods=["GET"])
def get_character(id):
    character = models.Character.get_by_id(id)
    print(character.__dict__)

    return jsonify(
        data = model_to_dict(character),
        status = 200,
        message = "Found the character"
    ), 200


# Update
@characters.route("/<id>", methods=["PUT"])
def update_character(id):
    payload = request.get_json()
    query = models.Character.update(**payload).where(models.Character.id == id)
    query.execute()
    response = model_to_dict(models.Character.get_by_id(id))
    return jsonify(
        data = response,
        status = 200,
        message = "Character updated"
    ), 200


# Delete
@characters.route("/<id>", methods=["DELETE"])
def delete_character(id):
    query = models.Character.delete().where(models.Character.id == id)
    query.execute()
    return jsonify(
        data = "Character deleted",
        message = "Character deleted",
        status = 200,
    ), 200
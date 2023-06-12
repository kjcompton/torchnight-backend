from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
import models

characters = Blueprint('characters', 'character')
# All Characters
@characters.route("/", methods=["GET"])
def get_all_characters():
    characters = [model_to_dict(character) for character in models.Character.select()]
    return jsonify(
        data=characters, 
        status={"code": 200, "message": "Success"})


# Characters by owner
@characters.route("/test/<id>", methods=["GET"])
def get_characters_by_owner(id):
    # Join query to find all characters with the user id
    query = models.Character.select().join(models.User).where(models.User.id == id)
    characters = [model_to_dict(character) for character in query]
    return jsonify(
        data=characters, 
        status={"code": 200, "message": "Success"})


# Create character
@characters.route("/", methods=["POST"])
def create_character():
    payload = request.get_json()
    new_character = models.Character.create(
        owner=payload["id"], 
        name=payload["name"],
        image=payload["image"],
        characterClass=payload["characterClass"],
        level=payload["level"],
        xp=payload["xp"],
        hp=payload["hp"],
        mp=payload["mp"],
        strength=payload["strength"],
        dexterity=payload["dexterity"],
        intelligence=payload["intelligence"],
        helm=payload["helm"],
        chest=payload["chest"],
        gloves=payload["gloves"],
        boots=payload["boots"],
        ring=payload["ring"],
        item1=payload["item1"],
        item2=payload["item2"],
        item3=payload["item3"],
        item4=payload["item4"],
        item5=payload["item5"]
    )
    print(new_character)

    character_dict = model_to_dict(new_character)

    print(character_dict)

    
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
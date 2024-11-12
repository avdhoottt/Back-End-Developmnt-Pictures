from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES (LIST)
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """
    List all pictures
    Returns the data list with HTTP_200_OK
    """
    return jsonify(data), 200

######################################################################
# GET A PICTURE (READ)
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """
    Read a picture by its ID
    Returns HTTP_404_NOT_FOUND if not found
    Returns picture with HTTP_200_OK if found
    """
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    
    return {"message": "picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """
    Create a new picture
    Returns HTTP_302_FOUND if picture exists
    Returns HTTP_201_CREATED if picture created successfully
    """
    picture_in = request.get_json()
    
    # Check if picture already exists
    for picture in data:
        if picture["id"] == picture_in["id"]:
            return {"Message": f"picture with id {picture_in['id']} already present"}, 302
    
    # Add new picture
    data.append(picture_in)
    return jsonify(picture_in), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """
    Update a picture by its ID
    Returns HTTP_404_NOT_FOUND if picture not found
    Returns HTTP_201_CREATED with updated picture if successful
    """
    updated_picture = request.get_json()
    
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = updated_picture
            return jsonify(updated_picture), 201
    
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """
    Delete a picture by its ID
    Returns HTTP_404_NOT_FOUND if picture not found
    Returns HTTP_204_NO_CONTENT with empty string if successful
    """
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data.pop(i)
            return "", 204
    
    return {"message": "picture not found"}, 404

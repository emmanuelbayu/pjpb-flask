from flask import Flask, request, url_for, redirect, session, jsonify
from db import mongo
from authlib.integrations.flask_client import OAuth
import os
from google.oauth2 import id_token
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo.init_app(app) #Mongodb config

@app.route("/")
def index():
    return "<h1> Hello! </h1>" 

#ADD A USER
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "GET":
        return "<h1>Adding user</h1>"
    
    elif request.method == "POST":
        email = request.json["email"]
        uid = request.json["uid"]
        display_name = request.json["display_name"]
        photo_url = request.json["photo_url"]
        kontak = request.json["kontak"]
        alamat =request.json["alamat"]
        
        users_collection = mongo.db.user
        users_collection.insert_one({
            'email' : email,
            'uid' : uid,
            'display_name' : display_name,
            'photo_url' : photo_url,
            'kontak' : kontak,
            'alamat' : alamat
        })
        
        value = ({
            'email' : email,
            'uid' : uid,
            'display_name' : display_name,
            'photo_url' : photo_url,
            'kontak' : kontak,
            'alamat' : alamat
        })
        return value

#UPDATE USER DISPLAY NAME   
@app.route("/update_user/<display_name>")
def update_user(display_name):
    users_collection = mongo.db.user
    users_update = users_collection.find_one({"display_name" : display_name})
    users_update["display_name"] = "johny sins"
    users_collection.save(users_update)
    return "<h1>User updated successfully</h1>"

#DELETE USER
@app.route("/delete_user/<display_name>")
def delete_user(display_name):
    users_collection = mongo.db.user
    users_collection.delete_one({"display_name" : display_name})
    return "<h1>User deleted sucessfully</h1>"

if __name__ == '__main__':
    app.run(debug=True)

from calendar import c
from flask import Flask, request, g
from pyasn1.type.univ import Null
from db import mongo
import os
import requests
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import wraps

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo.init_app(app) #Mongodb config

@app.route("/")
def index():
    return "<h1> Hello! </h1>" 

def middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        request_google = requests.Request()
        headers = request.headers.get('authorization')
        if headers is None:
            return {'message' : 'No token'},400
        try:
            token = headers.split(" ")[1]
            id_info = id_token.verify_oauth2_token(
                token, request_google, [os.getenv('ANDROID_CLIENT_ID'), os.getenv('IOS_CLIENT_ID')])
            g.user_info = id_info
            return func(*args, **kwargs)
        except:
            message = {
                'message' : 'Authentication Failed',
            }
            return message, 403
    return decorated_function

#ADD A USER
@app.route("/add_user", methods=["POST", "GET"])
@middleware
def add_user():
    if request.method == "GET":
        return "<h1>Adding user</h1>"
    
    elif request.method == "POST":
        email = request.json["email"]
        uid = request.json["uid"]
        username = request.json["username"]
        display_name = request.json["display_name"]
        photo_url = request.json["photo_url"]
        kontak = request.json["kontak"]
        alamat =request.json["alamat"]
        
        users_collection = mongo.db.user
        users_collection.insert_one({
            'email' : email,
            'uid' : uid,
            'username' : username,
            'display_name' : display_name,
            'photo_url' : photo_url,
            'kontak' : kontak,
            'alamat' : alamat
        })
        value = ({
            'email' : email,
            'uid' : uid,
            'username' : username,
            'display_name' : display_name,
            'photo_url' : photo_url,
            'kontak' : kontak,
            'alamat' : alamat
        })
        return value

#UPDATE USER DISPLAY NAME   
@app.route("/update_user/", methods=["POST"])
# @middleware
def update_user():
    users_collection = mongo.db.user
    uid = request.json['uid']
    display_name = request.json['display_name']
    users_update = users_collection.find_one({"uid" : uid})
    users_update["display_name"] = display_name
    users_collection.save(users_update)
    message = {
        'message' : 'User updated'
    }
    return message

if __name__ == '__main__':
    app.run(debug=True)

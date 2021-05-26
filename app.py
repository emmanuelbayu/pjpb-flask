from flask import Flask
from db import mongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbAdmin:demuji@pjpb.d1llr.mongodb.net/lapor?retryWrites=true&w=majority"

mongo.init_app(app)

@app.route("/")
def index():
    return "<h1> Hello! </h1>" 

#ADD A USER
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    users_collection = mongo.db.user
    users_collection.insert_one({
        "email" : "test",
        "uid" : "test",
        "display_name" : "adasdasd",
        "photo_url" : "test",
        "kontak" : "14045",
        "alamat" : "surga"
    })
    return "<h1>User added successfully</h1>"

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

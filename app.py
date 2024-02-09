from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymongo
from datetime import datetime
from pprint import pprint
import os
from openai import OpenAI

load_dotenv()
COSMOS_CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY_MIC24")

mongo_client = pymongo.MongoClient(COSMOS_CONNECTION_STRING)
db1 = mongo_client["db1"]
coll_dev = db1["coll_robots2"]

openAI_client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/api/robot", methods=["GET", "POST"])
def post_route_robot():
    print("Processing user request.")
    user_robot = request.json
    user_robot["dateCreated"] = datetime.now()
    user_notes = user_robot["notes"]
    response = openAI_client.images.generate(
        model="dall-e-3",
        prompt=user_notes,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    print(image_url)
    user_robot["image_url"] = image_url
    _ = coll_dev.insert_one(user_robot)
    return {"data": "success"}

@app.route("/api/robots", methods=["GET"])
def get_robots():
    msg_dict = {"data":{"assembly":[], "name":[], "notes":[], "imageUri":[]}}
    for doc in coll_dev.find():
        print(doc.keys())
        print(doc)
        if doc.get("data") is not None:
            print(doc["data"])
            msg = ''
            for item in doc["data"]:
                msg += '['+item["name"]+']'
                msg += '&rarr;'
            robot_name = ""
            if doc.get("name") is not None:
                robot_name += doc.get("name")
            robot_notes = ""
            if doc.get("notes") is not None:
                robot_notes += doc.get("notes")
            msg_dict["data"]["assembly"].append(msg)
            msg_dict["data"]["name"].append(robot_name)
            msg_dict["data"]["notes"].append(robot_notes)
            # print(doc["image_url"])
            msg_dict["data"]["imageUri"].append(doc["image_url"])
    return msg_dict

@app.route("/view/student_side")
def view_student_side():
    return render_template("student_side.html")

@app.route("/view/company_side")
def view_company_side():
    for doc in coll_dev.find():
        pprint(doc)
    return render_template("company_side.html")

if __name__ == "__main__":
    app.run(debug=True)

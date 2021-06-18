# author:Prathamesh Deogharkar
import threading
from database_config import init_db
from detect_face import detectentry
# from delete_face import delete_embedding
import pickle
import os
from services import create_user_dataset,delete_embedding,GenerateDeviceID,auth_deviceID,getLanding
import socket
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from flask_jsglue import JSGlue
import cv2
import numpy as np
from train_model import train_embedding
import logging

app = Flask(__name__)
JSGlue(app)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
path = os.path.dirname(os.path.realpath(__file__))
recognizer = pickle.loads(open(path + "/recognizer.pickle", "rb").read())
le = pickle.loads(open(path + "/le.pickle", "rb").read())
lelock = threading.Lock()
dataLock = threading.Lock()

print("Recognizer============>>",recognizer)
print("Le===================>>",le)

@app.route('/')
def hello_world():
    return ("Hello World")


@app.route('/register')
def register_user():
    # return render_template("Registration_del.html")
    return render_template("Registration.html")

@app.route('/recognize',methods=["POST"])
def recognize_face():
    data=request.form.getlist("image")
    lowAcc=request.form.get("low_acc")
    # action= "intime"
    # print("Location======>>",request.form.get("location"))
    print("DeviceID=======>>",request.form.get("deviceID"))
    print("config=======>>", request.form.get("config"))
    if(len(data)>0):
        result=detectentry(data,recognizer,le,lelock,int(lowAcc),request.form.get("location"),request.form.get("deviceID"),request.form.get("config"))
        print("result=======>",result)
        return jsonify({"result": "Done","value":result[0],"name":result[1]})
    else:
        return jsonify({"result":"Error"})

@app.route('/detect_face_in',methods=["GET","POST"])
def detect_face_in():
    if request.method=="GET":
        return render_template("Recognize.html",data="3117TS202106060243")
    else:
        data=request.form.get("deviceID")
        loc=request.form.get("loc")
        # data1=request.form.get("lastname")
        print(data)
        return render_template("Recognize.html",data=data,loc=loc)

@app.route('/detect_face_out',methods=["GET","POST"])
def detect_face_out():
    if request.method=="GET":
        return render_template("Recognize_out.html",data="3117TS202106060243")
    else:
        data=request.form.get("deviceID")
        loc = request.form.get("loc")
        comment = request.form.get("data")
        # data1=request.form.get("lastname")
        print("DeviceID=========>>",data)
        return render_template("Recognize_out.html",data=data,loc=loc)




@app.route('/train',methods=["GET"])
def train():
    return Response(train_embedding(recognizer, le, lelock, dataLock, "/EmployeeDataset"),content_type='text/event-stream')

@app.route('/auth_device',methods=["POST"])
def auth_device():
    data=request.get_json()
    print("Data=======>>",data["deviceID"])
    if data["deviceID"] != "":
        resp=auth_deviceID(data["deviceID"])
        print("Controler value====>",resp)
        if(resp):
            return jsonify({"data":"true"})
        else:
            return jsonify({"data": "false"})
    else:
        return jsonify({"data": "false"})


@app.route('/gen_deviceId',methods=["POST"])
def gen_DeviceId():
    data=request.get_json()
    print(data)
    if  data["ecn"]=="" or data["location"]=="" or data["name"]=="":
        return jsonify({"status":"missing Field"})
    else:
        data= GenerateDeviceID(data)
        return jsonify({"data":data})


@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.form.getlist('image')
        ecn = request.form.get('ecn')
        lable = request.form.get('number')
        return jsonify(create_user_dataset(data, lable, ecn))
    except Exception as ex:
        logging.exception("An exception occured=====>>")
        return jsonify({"result": "Error", "status": 500})
    # for a in range(10):
    #     frame = cv2.imdecode(
    #         np.frombuffer(base64.b64decode(data[a].split(',')[1]), dtype=np.uint8),
    #         flags=cv2.IMREAD_COLOR)
    #     cv2.imwrite(str(request.form.get('number')) + '.png', frame)
    #     return jsonify({"result": "Done", "status": 200})

@app.route('/del',methods=["POST"])
def delete():
    print(request.form.get("id"))
    if delete_embedding(request.form.get("id")):
        return Response(train_embedding(recognizer, le, lelock, dataLock, "/Empty"),content_type='text/event-stream')
    else:
        return jsonify({"status":200})

@app.route('/landing',methods=["GET","POST"])
def landing():
    print(request.args.get("id"))
    if not (request.args.get("id")):
        return jsonify({"result": "Error"})
    else:
        result =getLanding(request.args.get("id"))
        return render_template("Landing.html", data= result)



if __name__ == '__main__':
    init_db()
    app.run(debug=True)

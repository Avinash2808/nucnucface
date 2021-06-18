import cv2
import base64
import numpy as np
import os
from os import path
import pickle
import threading
import random
import string
from models import device_master,attendance_master
import datetime
from datetime import  date
from database_config import db_session
from repository import device_master_Repository,attendance_master_Repository


abspath = "EmployeeDataset/"
abspath_in = "C:/Users/3117/PycharmProjects/pythonProject/SuccCase"
image_count=1

def create_user_dataset(data, lable, ecn):
    global image_count
    print(lable,image_count)
    print(type(lable))
    if int(lable) == image_count:
        print("Increase lable val b4",image_count)
        image_count=int(lable)+1
        print("Increase lable val after",image_count)
    else:
        image_count=image_count+1

    folder=abspath+ecn+"/"
    if create_dir(ecn):
        for a in range(len(data)):
            frame = cv2.imdecode(
                np.frombuffer(base64.b64decode(data[a].split(',')[1]), dtype=np.uint8),
                flags=cv2.IMREAD_COLOR)
            cv2.imwrite(folder+str(image_count) + '.png', frame)
            return {"result": "Done", "status": 200}


def create_dir(ecn):
    if path.exists(abspath + ecn):
        return True
    else:
        os.mkdir(abspath+ecn)
        print("Dir is Created")
        return True

def create_SuccCase(data,ecn,a):
    print("Inside create_SuccCase")
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=7))
    print("Name of Image======>>",res)
    x = datetime.datetime.now()
    image_name=ecn+"_"+res + '.png'
    # reg = Register(ecn,image_name,str(a),x)
    # mark_entry(reg)
    for a in range(len(data)):
        frame = cv2.imdecode(
            np.frombuffer(base64.b64decode(data[a].split(',')[1]), dtype=np.uint8),
            flags=cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (600, 600),
                           interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(abspath_in + image_name, frame)
        print("Saved Image",image_name)


def mark_entry(reg):
    # print("Inside mark_entry",ecn,name)
    db_session.add(reg)
    db_session.commit()

def GenerateDeviceID(data):
    print(data)
    # name= data["name"]
    deviceId=data["ecn"]+data["location"]
    x = date.today()
    d1=x.strftime("%Y%m%d")
    res = ''.join(random.choices(string.digits, k=4))
    deviceId=deviceId+d1+res
    print(deviceId)
    data = device_master(data["ecn"], x, deviceId)
    resp = device_master_Repository.device_master(data)
    return resp

def attendance_captured(ecn,deviceid,location,comments,action):
    print("Inside attendance captured services")
    x = date.today()
    d1=x.strftime("%Y%m%d")
    print("date is=======>",d1)
    t= datetime.datetime.now()
    current_time = t.strftime("%H:%M:%S")
    data1 = attendance_master(ecn,str(d1),deviceid,current_time,location,action,"xyz")
    # print("data1=====>",data1)

    resp1 =attendance_master_Repository.attendance_master(data1)

    print("response1======>",resp1)
    return resp1

def auth_deviceID(deviceID):
    action=""
    d1 = date.today().strftime("%Y-%m-%d")
    data=device_master_Repository.authDevice(deviceID)
    config=attendance_master_Repository.checkIfExistConfig(deviceID,d1)
    if config:
        action="intime"
    else:
        action = "outtime"
    return [data,action]

def getLanding(id):
    AttendanceUser=[]
    print("SERVICE=====>",id)
    result = attendance_master_Repository.getall(id)
    for i in result:
        user=[]
        user.append(str(i.ecn))
        user.append(str(i.date))
        user.append(str(i.time))
        user.append(str(i.deviceid))
        # user.append(str(i.location))
        user.append(str(i.action))
        user.append(str(i.comments))
        AttendanceUser.append(user)
    return AttendanceUser


def delete_embedding(data_id):
    print("Inside Delete User")
    # path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(os.path.realpath(__file__))
    outer_recognizer = pickle.loads(open(path + "/recognizer.pickle", "rb").read())
    outer_le = pickle.loads(open(path + "/le.pickle", "rb").read())
    lelock = threading.Lock()
    dataLock = threading.Lock()
    data = pickle.loads(open(path + "/Facenet_embeddings.pickle", "rb").read())
    knownEncodings = data['encodings']
    knownNames = data['names']
    with dataLock:
        if os.path.isdir(path):
            res_list = [j for j, value in enumerate(data['names']) if value == str(data_id)]
            try:
                print(res_list)
                for j in reversed(res_list):
                    # print(j)
                    del data['encodings'][j]
                    # print(j)
                    del data['names'][j]
                f = open(path + "/Facenet_embeddings.pickle", "wb")
                f.write(pickle.dumps(data))
                f.close()
                return True

            except Exception as e:
                print(e)
                pass



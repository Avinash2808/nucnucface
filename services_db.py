from models import *
from repository import *
from datetime import datetime
import json
import ast

class User_Service:
    def create_user(ecn,name):
        user=User(ecn,name)
        User_Repository.create_user(user)
        print(ecn,name)

class device_master_Service:
    def device_master(ecn,datetime,deviceid):
        data=device_master(ecn,datetime,deviceid)
        device_master_Repository.device_master(data)
        print(ecn,datetime,deviceid)


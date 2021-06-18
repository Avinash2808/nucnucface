from database_config import db_session, engine
from sqlalchemy.orm import sessionmaker
from models import *

Session = sessionmaker(bind=engine)
session = Session()

# class Register_Repository:
#     def register(user):
#         db_session.add(user)
#         db_session.commit()
#         return True



# class User_Repository:
#     def create_user(user):
#         db_session.add(user)
#         db_session.commit()

class device_master_Repository:
    def device_master(data):
        print(data.ecn)
        result=session.query(device_master).filter(device_master.ecn==data.ecn).first()
        # print(result.deviceid)
        if not result:
            db_session.add(data)
            db_session.commit()
            return data.deviceid
        else:
            print("Already Exist")
            return result.deviceid

    def authDevice(deviceid):
        result = session.query(device_master).filter(device_master.deviceid == deviceid).first()

        if not result:
            print("Sending False")
            return False
        else:
            print(result.ecn)
            print("Sending True")
            return True

class attendance_master_Repository:
    def attendance_master(att_data):
        print("Inside att master repository")
        res = attendance_master_Repository.checkIfExist(att_data.ecn,att_data.date,att_data.action)
        if (res):
            result=session.query(device_master).filter(device_master.ecn==att_data.ecn).first()


            # print("ecn=====>",att_data.ecn)
            print("action in att repositiry=====>", att_data.action)
            db_session.add(att_data)
            db_session.commit()
            print("Inside repositiry")
            print("result====>",result.name)
            return result.name
            # return data1.
        else:
            result = session.query(device_master).filter(device_master.ecn == att_data.ecn).first()
            return result.name

    def checkIfExist(ecn,date,action):
        result = session.query(attendance_master).filter(attendance_master.ecn==ecn,attendance_master.date == date,attendance_master.action==action).first()
        if not result:
            print ("Not Present")
            return  True
        else:
            print("Attendance already marked====>",result.ecn,result.date,result.time)
            return  False

    def checkIfExistConfig(deviceID,date):
        result = session.query(attendance_master).filter(attendance_master.deviceid == deviceID,attendance_master.date==date,attendance_master.action=="intime").first()
        if not result:
            print("Not Present")
            return True
        else:
            print("Attendance Already Marked=====>>",result.ecn, result.date,result.time)
            return False

    def getall(id):
        print("REPO======>>",id)
        result = session.query(attendance_master).filter(attendance_master.ecn ==id)
        return result
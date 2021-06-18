
from sqlalchemy import *
from database_config import Base


# class Register(Base):
#     __tablename__ = 'register_master'
#     id = Column(Integer, primary_key=True)
#     emp_id = Column(String(50), nullable=False)
#     image_name = Column(String(50), nullable=False)
#     accuracy= Column(String(50), nullable=False)
#     time_stamp= Column(String(50))
#
#     def __init__(self, emp_id=None, image_name=None,accuracy=None,time_stamp=None):
#         self.emp_id = emp_id
#         self.image_name = image_name
#         self.accuracy=accuracy
#         self.time_stamp=time_stamp
#
#
#     def __repr__(self):
#         return ("Attendance====>{0},{1},{2}").format(self.emp_id, self.image_name)

# class User(Base):
#     __tablename__ = 'users_master'
#     id = Column(Integer, primary_key=True)
#     ecn = Column(String(50), unique=True)
#     name = Column(String(50))
#     # email = Column(String(120), unique=True)
#
#     def __init__(self, ecn = None,name=None):
#         self.ecn = ecn
#         self.name = name
#         # self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % (self.name)

class device_master(Base):
    __tablename__ = 'device_masters'
    id = Column(Integer, primary_key=True,autoincrement=True)
    deviceid = Column(String(50), unique=True)
    ecn = Column(String(50), unique=True)
    name = Column(String(50))
    datetime = Column(String(50))

    # email = Column(String(120), unique=True)

    def __init__(self, ecn = None,datetime=None,deviceid=None,name=None):
        self.ecn = ecn
        self.datetime = datetime
        self.deviceid=deviceid
        self.name = name
        # self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

class attendance_master(Base):
    __tablename__ = 'attendance_captured'
    id = Column(Integer, primary_key=True,autoincrement=True)
    ecn = Column(String(50))
    deviceid = Column(String(50))
    location = Column(String(50))
    date = Column(String(50))
    time = Column(String(50))
    action = Column(String(50))
    comments = Column(String(200))


    # email = Column(String(120), unique=True)

    def __init__(self, ecn = None,date=None,deviceid=None,time=None,location=None,action=None,comments=None):
        self.ecn = ecn
        self.date = date
        self.deviceid=deviceid
        self.time = time
        self.location= location
        self.action = action
        self.comments = comments
        # self.email = email

    # def __repr__(self):
    #     return '<User %r>' % (self.ecn)
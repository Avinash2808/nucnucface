import cv2
import base64
import numpy as np
from keras_facenet import FaceNet
import pickle
import os
from services import attendance_captured
embedder = FaceNet()
# path = os.path.dirname(os.path.realpath(__file__))
# recognizer1= pickle.loads(open(path + "/recognizer.pickle", "rb").read())
# counter=0
def detectentry(_image, recognizer, le, lelock,low_acc,location,id,action):
    # global counter
    # if(counter<1 or counter>5):
    #     counter=0;

    print("Detect Entry",len(_image))
    path = os.path.dirname(os.path.realpath(__file__))
    # recognizer1 = pickle.loads(open(path + "/recognizer.pickle", "rb").read())
    # le1 = pickle.loads(open(path + "/le.pickle", "rb").read())
    ecn = None
    # global ecnList
    # global UnknownFrameCount
    # global LastUnknownDetectionTime
    # global recognizer
    # global le
    # global lelock
    # print(os.getpid())
    # print(threading.get_ident())

    boxes = []

    tempData = {}

    try:

        # with lock:

        imageList = _image
        # print("Length of ImageList===>>", len(imageList))
        # clientIP = request.form.getlist('clientIP')[0]

        for a in range(len(imageList)):

            # start = time.time()

            frame = cv2.imdecode(
                np.frombuffer(base64.b64decode(imageList[a].split(',')[1]), dtype=np.uint8),
                flags=cv2.IMREAD_COLOR)

            frame = cv2.resize(frame, (600, 600),
                               interpolation=cv2.INTER_NEAREST)

            (he, wi) = None, None
            if np.shape(frame) != ():
                # print("I m inside NP.Shape")
                (he, wi) = frame.shape[:2]
            # (h, w) = frame.shape[:2]

            detections = embedder.extract(frame, threshold=0.95)
            # print("detections===========>",detections)
            margin = 5

            if not detections:
                print("Inside Not Detected")
                return ["N",""]

                # self.read_lock.acquire()
                # self.Attendance = attendance
                # self.read_lock.release()

            if detections:
                print("Inside Detected")
                # (top, right, bottom, left) = detections[0]['box']
                x, y, w, h = detections[0]['box']
                x -= margin
                y -= margin
                w += 2 * margin
                h += 2 * margin
                if x < 0 or y < 0 or x + w >= wi or y + h >= he:
                    print("No FACE FOUND IN FRAME")
                #     w += x
                #     x = 0
                # if y < 0:
                #     h += y
                #     y = 0

                with lelock:
                    preds = recognizer.predict_proba(detections[0]['embedding'].reshape(1, -1))[0]
                # embedder.crop()
                # print(preds)
                j = np.argmax(preds)
                a = np.max(preds)
                print(j,a)
                # print(le1.classes_, ecn)
                #recognizer[0]{3117}
                # proba = preds[j]
                if a > 0.64 or low_acc>=2:
                    print("Value of face recognize accuracy=========>>", a,j,location,id)
                    # print(le1.classes_, ecn)
                    with lelock:
                        ecn = le.classes_[j]
                        print("ECN====>>",ecn)
                        print("Le class data====>>", le.classes_)
                        data_name=attendance_captured(ecn,id,location,"abcde",action)
                        return [ecn,data_name]
                        # print(le1.classes_, ecn)
                elif (a > 0.4) and (a <= 0.64):
                    print('Maybe Low accuracy')
                    print("Value of face recognize accuracy========>>", a , low_acc)
                    print(le.classes_[j])
                    print(ecn)
                    return ["L",""]



                else:
                    print(a)
                    print("INSIDE ELSE ECN = NA")
                    ecn = 'NA'
                    return ["",""]



                # (left, top, right, bottom) = (x, y, x + w, y + h)

                # cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h),
                #               (0, 0, 255), 2)
                # cv2.putText(frame, str(ecn), (x1, y1),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # cv2.rectangle(frame, (left, top - 50), (right, top - 5), (253, 254, 254), -1)
                #
                # if ecn != 'NA':
                #     # create_SuccCase(_image,ecn,a)
                #     print("ECN====>>", ecn)
                #     return ecn
                #
                # else:
                #     return ""




    except Exception as e:
        print(e)



import threading

from keras_facenet import FaceNet
import os
from imutils import paths
import cv2
import pickle

from scipy.special import kn
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC, LinearSVC
import copy

# from thundersvm import SVC

a = 1
svcModel = SVC(kernel='linear', probability=True)


# svcModel = LinearSVC(random_state=0, tol=1e-5)
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

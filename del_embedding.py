import os
import pickle
def delete_embedding(ecn):

    global dataLock
    path = os.path.dirname(os.path.realpath(__file__))
    data = pickle.loads(open(path + "\Facenet_embeddings.pickle", "rb").read())
    with dataLock:
        if os.path.isdir(path):
            res_list = [j for j, value in enumerate(data['names']) if value == str(ecn)]
            try:
                for j in reversed(res_list):
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


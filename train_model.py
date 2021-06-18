from keras_facenet import FaceNet
import os
from imutils import paths
import cv2
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC, LinearSVC
import copy

# from thundersvm import SVC

a = 1
svcModel = SVC(kernel='linear', probability=True)


# svcModel = LinearSVC(random_state=0, tol=1e-5)
def train_embedding(outer_recognizer, outer_le, lelock, dataLock,folder):

    global svcModel
    print(outer_recognizer)
    embedder = FaceNet()

    path = os.path.dirname(os.path.realpath(__file__))
    imagePaths = list(paths.list_images(path + folder))
    #[3117,3118]
    data = pickle.loads(open(path + "/Facenet_embeddings.pickle", "rb").read())
    # data = open(path + "/Facenet_embeddings", "wb")
    knownEncodings = data['encodings']
    knownNames = data['names']
    print("======>",(type(data),type(knownNames),type(knownEncodings)))

    print("Known Names=========>>",knownNames)
    # print("Known Encodings=========>>", knownEncodings)
    print("Known Name Len=========>>", len(knownNames))
    print("Known Encodings Len=========>>", len(knownEncodings))
    # print("Known Encodings Embedding Len=========>>", len(knownEncodings[0]))
    # print(imagePaths)
    for (i, imagePath) in enumerate(imagePaths):
        print("ImagePAth===========>>", imagePath.split(os.path.sep))
        print(knownNames.count(imagePath.split(os.path.sep)[-2]),imagePath)
        if knownNames.count(imagePath.split(os.path.sep)[-2]) >= 100:
            print("Inisde if 100 block")
            yield "data: %d\n\n" % (((i + 1) * 100 / len(imagePaths)) - 1)
            continue

        name = imagePath.split(os.path.sep)[-2]

        image = cv2.imread(imagePath)

        if image is None:
            continue

        detections = embedder.extract(image, threshold=0.95)

        if detections:
            print("I M INSiDE Detection")
            print(str(detections[0]['confidence']))
            knownEncodings.append(copy.deepcopy(detections[0]['embedding'].flatten()))
            knownNames.append(copy.deepcopy(name))
        else:
            print(imagePath)

        yield "data: %d\n\n" % (((i + 1) * 100 / len(imagePaths)) - 1)

    print("Entering Data Lock")
    with dataLock:
        print("In Data Lock")
        data = {"encodings": copy.deepcopy(knownEncodings), "names": copy.deepcopy(knownNames)}
    print("Exited Data Lock")
    dataTemp = {"encodings": knownEncodings, "names": knownNames}
    print("Writing into Facenet pic")
    f = open(path + "/Facenet_embeddings.pickle", "wb")
    f.write(pickle.dumps(dataTemp))
    f.close()

    print("Writing into Facenet pic done")

    le = LabelEncoder()
    le1 = LabelEncoder()

    print("le fir transform")
    print(set(dataTemp["names"]))
    labels = le.fit_transform(copy.deepcopy(dataTemp["names"]))
    print(set(labels))
    # labels1 = le1.fit_transform(copy.deepcopy(dataTemp["names"]))

    try:
        print("Entering le Lock")
        with lelock:
            print("In le Lock")
            outer_le.fit_transform(copy.deepcopy(dataTemp["names"]))
            print("In le Lock 2")
            outer_recognizer.fit(copy.deepcopy(dataTemp['encodings']), copy.deepcopy(labels))
            # print(x)
            print("Exited le Lock")
        print("model fir transform")
        print(len(dataTemp['encodings']), len(labels))

    except Exception as e:
        print(e)

        # outer_le = copy.deepcopy(le)
        # outer_recognizer = copy.deepcopy(model)
    # with lelock:
    #     outer_le = copy.deepcopy(le)
    # print(outer_le.classes_)

    # outer_recognizer = copy.deepcopy(model)
    # # predict
    # yhat_train = model.predict(data['encodings'])
    # # yhat_test = model.predict(emdTestX_norm)
    # # data['names'] = np.array(data['names'])
    # score_train = accuracy_score( labels,yhat_train)
    # # score_test = accuracy_score(testy_enc, yhat_test)
    # # summarize
    # print('Accuracy: train=%.3f' % (score_train*100))
    print("Writing into rec pic")
    f = open(path + "/recognizer.pickle", "wb")
    with lelock:
        f.write(pickle.dumps(outer_recognizer))
    f.close()
    print("Writing into le pic")
    # write the label encoder to disk
    f = open(path + "/le.pickle", "wb")
    f.write(pickle.dumps(le))
    f.close()
    print("Training completed")

    yield "data: %d\n\n" % int(100)

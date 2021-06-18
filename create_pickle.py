import pickle

db = {}
db['encodings'] = []
db['names'] = []

# Its important to use binary mode
dbfile = open('Facenet_embeddings.pickle', 'ab')
pickle.dump(db, dbfile)
dbfile.close()


dbfile = open('Facenet_embeddings.pickle', 'rb')
db = pickle.load(dbfile)
for keys in db:
    print(keys, '=>', db[keys])
dbfile.close()

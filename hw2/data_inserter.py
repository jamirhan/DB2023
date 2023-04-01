import pymongo


client = pymongo.MongoClient('localhost', 27017)

db = client.wine
documents = []

with open("data.csv", "r") as data:
    names = [x[1:-1 if x != '"quality"\n' else -2]
             for x in data.readline().split(";")]
    print(names)
    for line in data:
        values = line.split(";")
        value = {}
        for ind in range(len(values)):
            value[names[ind]] = float(values[ind])
        documents.append(value)

db.test.insert_many(documents)

import pymongo

client = pymongo.MongoClient()
db = client['starwars']

luke = db.characters.find_one({"name":"Luke Skywalker"})

droids = db.characters.find({"species.name":"Droid"})
for droid in droids:
    print(droid)

print("\n")
dv = db.characters.find_one({"name":"Darth Vader"},{"height":1,"_id":0})["height"]
print(f"Darth Vaders height: {dv}cm")

print("\nNames of characters with yellow eyes")
yellow_eyes = db.characters.find({"eye_color":"yellow"},{"name":1,"_id":0})
for character in yellow_eyes:
    print(character["name"])

print("\nFirst 3 males")
males = db.characters.find({"gender":"male"})
for i in range(3):
    print(males.next()["_id"])

print("\nNames of Alderaanians")
alderanians = db.characters.find({"homeworld.name":"Alderaan","species.name":"Human"},{"name":1,"_id":0})
for alderanian in alderanians:
    print(alderanian["name"])

print("\nAverage height of female characters")
f_heights = db.characters.aggregate([{"$match":{"gender":"female"}},{"$group":{"_id":"$gender","avg_height":{"$avg":"$height"}}}])

print(f_heights.next())

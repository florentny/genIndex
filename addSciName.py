#!/usr/bin/python
import os
import sys

from pymongo import MongoClient


def getsci(lookup):
    if species.get(name) is not None:
        return species.get(name)
    res = dict(filter(lambda item: item[0] in lookup, species.items()))
    if len(res) == 1:
        return list(res.values())[0]
    res1 = dict(filter(lambda item: item[0] in lookup, alt.items()))
    if len(res1) == 1:
        return list(res1.values())[0]
    return None


client = MongoClient(port=27017)
db = client.reef4
species = {}
alt = {}
collection = db.species
for rec in collection.find({}, {"Name": 1, "sciName": 1, "_id": 0}):
    species[rec["Name"]] = rec['sciName']

for rec in collection.find({"aka": {"$exists": 1}}, {"aka": 1, "sciName": 1, "_id": 0}):
    alt[" ".join(rec["aka"])] = rec['sciName']

if not os.path.isfile("captions"):
    sys.exit("Cannot find captions file")

with open("captions") as f:
    for line in f:
        key, name = line.rstrip().split('|')
        if "(" in name:
            print(key + "|" + name)
            continue
        sciName = getsci(name)
        if sciName is None:
            print(key + "|" + name)
        else:
            print(key + "|" + name + " (" + sciName + ")")

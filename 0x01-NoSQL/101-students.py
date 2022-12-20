#!/usr/bin/env python3
"""
Write a Python function that returns all students sorted by average score
Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    function that returns all students sorted by average score
    """
    documents = list(mongo_collection.find())

    for doc in documents:
        total = 0
        for topic in doc["topics"]:
            total += topic["score"]
        avg = total / len(doc["topics"])

        name = doc["name"]
        avg_ = {"averageScore": avg}
        mongo_collection.update_many({"name": name}, {"$set": avg_})

    return mongo_collection.find().sort("averageScore", -1)

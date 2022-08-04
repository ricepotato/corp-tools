import os
import ssl
import pymongo
import configparser


def get_mongo_client(host, user, password):
    """mongodb+srv://ricepotato:<password>@cluster0-gpvm5.gcp.mongodb.net/wetube?retryWrit"""
    connection_string = f"mongodb+srv://{user}:{password}@{host}"
    client = pymongo.MongoClient(
        connection_string, ssl=True, tlsAllowInvalidCertificates=True
    )
    return client


def get_client():
    host = os.environ.get("MONGODB_HOST")
    user = os.environ.get("MONGODB_USER")
    password = os.environ.get("MONGODB_PASSWORD")
    client = get_mongo_client(host, user, password)
    return client


class MongoDao(object):
    def __init__(self):
        self.client = get_client()
        self.coll = self.client.qi.stock

    def insert(self, obj):
        return self.coll.insert_one(obj)

    def find_by_code(self, code):
        obj = self.coll.find_one({"code": code})
        return obj

    def get_stock_list(self, market, mc_min=None, mc_max=None):
        query_and = [{"market": market}]
        if mc_min is not None:
            query_and.append({"market_cap": {"$gte": mc_min}})

        if mc_max is not None:
            query_and.append({"market_cap": {"$lte": mc_max}})

        rs = self.coll.find({"$and": query_and}, {"_id": False})
        return list(rs)

    def set_object(self, code, object):
        return self.coll.update_one({"code": code}, {"$set": object})

    def exist(self, code, obj_notation):
        res = self.coll.find_one(
            {"$and": [{"code": code}, {obj_notation: {"$exists": True}}]}
        )
        if res:
            return True
        else:
            return False

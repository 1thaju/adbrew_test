"""MongoDB connection configuration."""

import os

from pymongo import MongoClient


mongo_client = MongoClient(
    host=os.environ["MONGO_HOST"],
    port=int(os.environ["MONGO_PORT"]),
)
db = mongo_client["test_db"]

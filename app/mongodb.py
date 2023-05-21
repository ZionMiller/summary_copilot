from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["phone_call_summaries"]
    collection = db["summaries"]
except ConnectionError as e:
    error_message = str(e)
except Exception as e:
    error_message = str(e)
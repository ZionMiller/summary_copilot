from pymongo import MongoClient

# The reason for moving this code to a separate file, mongodb.py, is to isolate the database-related functionality
# and make the code more modular and organized.
# We are also catching isolated errors related to this
#TODO move Mongo from community to Atlas to host API on AWS, community is just for our proof concept

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["phone_call_summaries"]
    collection = db["summaries"]
except ConnectionError as e:
    error_message = str(e)
except Exception as e:
    error_message = str(e)
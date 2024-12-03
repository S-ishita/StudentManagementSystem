from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://singhalishita016:test@studentmanagementsystem.5ep8k.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.students

student_collection = database.get_collection("students_collection")

def student_helper(student) -> dict:
    return {
        "name": student["name"],
        "age": student["age"],
        "address": {
            "city": student["address"]["city"],
            "country": student["address"]["country"]
        }
    }


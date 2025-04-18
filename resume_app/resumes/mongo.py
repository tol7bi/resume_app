from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['resume_analyzer']
collection = db['analyses']

def save_analysis(analysis_data):
    result = collection.insert_one(analysis_data)
    return result.inserted_id

def get_resume_analysis_for_user(user_email):
    return collection.find_one({'email': user_email}) or {}
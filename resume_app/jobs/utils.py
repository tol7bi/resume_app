from pymongo import MongoClient
from django.conf import settings
from .models import Job

# Устанавливаем подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['resume_analyzer']
collection = db['analyses']


def compute_match_score(user_skills, required_skills_str):
    if not user_skills or not required_skills_str:
        return 0

    user_set = set(skill.lower() for skill in user_skills)
    required_set = set(skill.strip().lower() for skill in required_skills_str.split(','))

    matched = user_set & required_set
    score = (len(matched) / len(required_set)) * 100
    return round(score, 2)


def get_matching_jobs(user_id):
    analysis_record = collection.find_one({'user_id': user_id}, sort=[('_id', -1)])
    if not analysis_record:
        return []

    extracted_skills = analysis_record.get('skills', [])
    all_jobs = Job.objects.all()
    results = []

    for job in all_jobs:
        match_score = compute_match_score(extracted_skills, job.required_skills)
        if match_score > 0:
            results.append({
                'job_id': job.id,
                'title': job.title,
                'description': job.description,
                'location': job.location,
                'required_skills': job.required_skills,
                'match_score': match_score,
            })

    return sorted(results, key=lambda item: item['match_score'], reverse=True)


def get_resume_analysis_for_user(user_email):
    analysis = collection.find_one({"user_email": user_email})

    if analysis:
        return {
            'skills': analysis.get('skills', []),
            'experience_summary': analysis.get('experience_summary', '')
        }
    return {}
from pymongo import MongoClient
import nltk
from PyPDF2 import PdfReader
import os
from docx import Document
import re

client = MongoClient('mongodb://localhost:27017/')
db = client['resume_analyzer']
collection = db['analyses']



nltk.download('punkt')

def save_analysis_to_mongo(data, user_email):
    data['user_email'] = user_email
    collection.insert_one(data)


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text

    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join(para.text for para in doc.paragraphs)

    return ''


def analyze_resume_text(text):
    words = nltk.word_tokenize(text)
    skills = extract_skills_from_text(text)
    experience = extract_experience_from_text(text)

    entities = extract_entities_simple(text)

    return {
        'entities': entities,
        'words': words,
        'skills': skills,
        'experience_summary': experience
    }


def extract_skills_from_text(text):
    skill_keywords = [
        'Python', 'Django', 'JavaScript', 'Java', 'SQL', 'HTML', 'CSS',
        'React', 'Node.js', 'AWS', 'Docker'
    ]
    found = []
    for keyword in skill_keywords:
        if keyword.lower() in text.lower():
            found.append(keyword)
    return found


def extract_experience_from_text(text):
    experience_keywords = ['experience', 'worked as', 'developed', 'managed', 'designed', 'led']
    sentences = nltk.sent_tokenize(text)
    relevant = [s for s in sentences if any(k in s.lower() for k in experience_keywords)]
    return ' '.join(relevant)


def extract_entities_simple(text):
    entities = []

    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    for e in emails:
        entities.append({'text': e, 'label': 'EMAIL'})

    dates = re.findall(r"\b\d{4}\b", text)
    for d in dates:
        entities.append({'text': d, 'label': 'YEAR'})

    phones = re.findall(r"\b(?:\+?\d{1,3})?\s?(?:\(?\d{2,4}\)?\s?)?\d{3}[-.\s]?\d{4}\b", text)
    for p in phones:
        entities.append({'text': p, 'label': 'PHONE'})

    return entities


def analyze_resume(user_email):
    analysis = collection.find_one({"user_email": user_email})
    if analysis:
        return {
            'skills': analysis.get('skills', []),
            'experience_summary': analysis.get('experience_summary', '')
        }
    return {}

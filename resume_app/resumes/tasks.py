from celery import shared_task
from .models import Resume

@shared_task
def parse_resume(resume_id):
    resume = Resume.objects.get(id=resume_id)
    resume.skills = 'parsed skills'
    resume.experience = 5
    resume.save()
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes_storage/')
    skills = models.TextField(blank=True)
    text_content = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)

    rating = models.FloatField(default=0.0)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — Resume {self.id}"




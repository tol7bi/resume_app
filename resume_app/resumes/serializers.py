from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'id', 'user', 'file', 'uploaded_at',
            'text_content', 'skills', 'experience', 'education',
            'rating', 'recommendations'
        ]
        read_only_fields = ['id', 'uploaded_at', 'text_content', 'skills', 'experience', 'education', 'rating', 'recommendations']

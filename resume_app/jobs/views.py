from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .serializers import JobSerializer
from .utils import get_matching_jobs
from .utils import get_resume_analysis_for_user


class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JobMatchingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        analysis_result = get_resume_analysis_for_user(user.email)

        extracted_skills = analysis_result.get('skills', [])

        if not extracted_skills:
            return Response(
                {"matches": [], "reason": "No skills found in resume"},
                status=200
            )

        user_skills = set(skill.lower() for skill in extracted_skills)
        matched_jobs = []

        for job in Job.objects.all():
            required = job.required_skills.split(',')
            required_skills = set(skill.strip().lower() for skill in required)

            if user_skills & required_skills:
                matched_jobs.append(JobSerializer(job).data)

        return Response({"matches": matched_jobs})


class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
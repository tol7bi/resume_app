from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Resume
from .serializers import ResumeSerializer
from .utils import analyze_resume, extract_text

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)

            text = extract_text(resume.file.path)
            analysis_result = analyze_resume(text)

            resume.text_content = text
            resume.skills = ", ".join(analysis_result.get('skills', []))
            resume.experience = analysis_result.get('experience', '')
            resume.education = analysis_result.get('education', '')
            resume.rating = analysis_result.get('rating', 0.0)
            resume.recommendations = analysis_result.get('recommendations', '')
            resume.save()

            return Response(ResumeSerializer(resume).data)
        return Response(serializer.errors, status=400)


class ResumeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

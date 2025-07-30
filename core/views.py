from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .audio_utils import transcribe_with_diarization
import tempfile
from rest_framework.decorators import api_view
from .title_suggest import suggest_titles

class TranscriptionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        audio = request.FILES.get("audio")
        if not audio:
            return Response({"error": "No audio file uploaded."}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            for chunk in audio.chunks():
                temp_audio.write(chunk)
            temp_audio_path = temp_audio.name

        result = transcribe_with_diarization(temp_audio_path)
        return Response(result)
    
@api_view(["POST"])
def title_suggestion(request):
    content = request.data.get("content", "")
    if not content:
        return Response({"error": "Blog content is required"}, status=400)
    
    titles = suggest_titles(content)
    return Response({"suggestions": titles})

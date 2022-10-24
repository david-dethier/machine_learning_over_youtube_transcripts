from rest_framework import mixins, serializers, viewsets
from youtube_transcript_api import YouTubeTranscriptApi

from api.v1.youtube.caption.exceptions import UnspecifiedVideo, VideoNotFound
from api.v1.youtube.caption.serializers import CaptionSerializer


class CaptionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CaptionSerializer
    
    
    def get_queryset(self):
        
        videoid = self.request.query_params.get("videoId", None)
        
        if videoid in {"", None}:
            raise UnspecifiedVideo()
        
        try:
            context = YouTubeTranscriptApi.get_transcript(
                    video_id=videoid, languages=["es", "en"]
            )
        except Exception:
            raise VideoNotFound(videoid)
        
        serializer = self.serializer_class(data=context, many=True)
        
        try:
            if serializer.is_valid(True):
                return serializer.validated_data
        except serializers.ValidationError as exc:
            return {exc.detail}
    
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

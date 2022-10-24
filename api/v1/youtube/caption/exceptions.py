from rest_framework.exceptions import APIException
from rest_framework import status


class VideoNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Could not retrieve a transcript for the video {video_id}!"
    default_code = "video_not_found"
    detail = None
    code = None

    def __init__(self, video_id, detail=None, code=None):
        if detail is None:
            self.detail = self.default_detail.replace("video_id", video_id)
        else:
            self.detail = detail
        if code is None:
            self.code = self.default_code
        else:
            self.code = code


class UnspecifiedVideo(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Video id not specified!"
    default_code = "unspecified_video"
    detail = None
    code = None

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail
        if code is None:
            self.code = self.default_code
        else:
            self.code = code

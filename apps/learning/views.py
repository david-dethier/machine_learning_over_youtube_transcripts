from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.learning.serializers import ExtraListSerializer
from rest_framework.exceptions import APIException


class LearningViewSet(viewsets.GenericViewSet):
    serializer_class = ExtraListSerializer
    
    
    def get_queryset(self):
        self.queryset = self.request.data
        return self.queryset
    
    
    def list(self, request):
        return Response(data="LLEGUE DESDE EL LIST", status=status.HTTP_200_OK)
    
    
    @action(methods=["POST"], detail=False)
    def extra_list(self, request):
        try:
            serializer = self.get_serializer(data=self.get_queryset())
            if serializer.is_valid():
                return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exc:
            return exc.detail

from rest_framework import serializers


class ExtraListSerializer(serializers.Serializer):
    email = serializers.EmailField()

from rest_framework import serializers
from api.v1.ai.translation.models import TranslationModel


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationModel
        fields = "__all__"

    def validate(self, attrs):
        ret = super().validate(attrs)
        return ret
        
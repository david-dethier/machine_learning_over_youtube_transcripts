from rest_framework import serializers


class DistilBartSerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=1024)
    
    
    def to_internal_value(self, data):
        val = {"input_text": data}
        return val

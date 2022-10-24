from rest_framework import serializers


class CaptionSerializer(serializers.Serializer):
	text = serializers.CharField(max_length=255)
	start = serializers.DecimalField(max_digits=10, decimal_places=3, min_value=0.0)
	duration = serializers.DecimalField(max_digits=10, decimal_places=3, min_value=0.0)
	
	
	def validate_text(self, attrs):
		# print(attrs)
		return super().validate(attrs)
	
	
	def validate_start(self, attrs):
		return super().validate(attrs)
	
	
	def validate_duration(self, attrs):
		return super().validate(attrs)
	
	
	def validate(self, attrs):
		ret = super().validate(attrs)
		return ret


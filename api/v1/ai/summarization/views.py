import timeit

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from core.decorators import benchmark
from .serializers import DistilBartSerializer


class DistilBartViewSet(viewsets.GenericViewSet):
    serializer_class = DistilBartSerializer
    
    
    def get_queryset(self):
        self.queryset = self.request.data["input_text"]
        return self.queryset
    
    
    @benchmark
    @action(detail=False, methods=['POST'])
    def distilbart(self, request):
        starting = timeit.default_timer()
        input_text = self.get_queryset()
        serializer = self.get_serializer(data=input_text)
        
        if serializer.is_valid(raise_exception=True):
            tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
            model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
            
            inputs = tokenizer.encode(serializer.validated_data["input_text"], return_tensors="pt", truncation=True)
            inputs_ids = model.generate(inputs, num_beams=2, min_length=0, max_length=512)
            summary = tokenizer.batch_decode(inputs_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[
                0]
            ending = timeit.default_timer() - starting
            
            return Response({"timing": ending, "summary": summary})
    
    
    def list(self, request):
        return Response("Vino desde el GET", status=status.HTTP_200_OK)

from time import sleep
from django.core.cache import cache
from core.decorators import benchmark
from api.v1.ai.translation.selectors import translate_mbart_large_50_many_to_many_mmt
from rest_framework import viewsets
from api.v1.ai.translation.serializers import TranslationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_q.models import Task, OrmQ
from django_q.tasks import result
from django_q.tasks import async_task
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotFound


def tasksimulation():
    sleep(30)
    print("TAREA TERMINADA")
    return "TAREA TERMINADA"


class TranslationViewSet(viewsets.GenericViewSet):
    serializer_class = TranslationSerializer
    basename = 'translation'
    
    
    @action(methods=["get"], detail=False, url_path="getit/(?P<task_id>\w+)")
    def getit(self, request, **kwargs):
        
        # you mustr construct the get url to take the id
        task_id = self.kwargs.get('task_id')
        
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None
        
        # here the task is on processing
        if task:
            return Response({
                'id': task_id,
                'result': result(task_id),
                'started': task.started,
                'stopped': task.stopped,
                'status': 'DONE' if task.stopped else 'RUNNING',
                'success': task.success,
            })
        else:
            # here you find the task in the query (not even processed, but waiting for the cluster to process it)
            for q in OrmQ.objects.all():
                if q.task_id() == task_id:
                    task = q.task()
                    return Response({
                        'id': task['id'],
                        'started': task['started'],
                        'status': 'WAITING',  # or ON QUEUE
                        'stopped': None,
                        'success': None,
                    })
        
        raise NotFound()
    
    
    @action(methods=["get"], detail=False)
    def translate(self, request):
        # serializer = self.get_serializer(data=request.data)
        serializer = self.get_serializer(data={
            "from_lang":
                "en_XX"
            ,
            "to_lang":
                "en_XX"
            ,
            "input":
                "Este campo es requerido."
            
        })
        if serializer.is_valid(raise_exception=True):
            cache.set('my_key', 'hello, world!', 60)
            print("CACHE =  ", cache.get('my_key'))
            
            task_id = async_task(tasksimulation)
            # # task_id = async_task(translate_mbart_large_50_many_to_many_mmt(**serializer.validated_data))
            # # link = reverse(viewname="translation-translate", request=request, kwargs={'task_id': task_id})
            link = reverse(viewname="translation-getit", request=request, kwargs={'task_id': task_id})
            # print(f'task_id : {task_id} > link : {link}')
            return Response(data={'task_id': task_id, 'link': link}, status=status.HTTP_200_OK)

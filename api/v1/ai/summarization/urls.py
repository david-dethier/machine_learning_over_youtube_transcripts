from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.ai.summarization import views

router = DefaultRouter()
router.register("summarization", views.DistilBartViewSet, basename="summarization")

urlpatterns = [
    path("/", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.youtube.caption import views

router = DefaultRouter()
router.register("transcript", views.CaptionViewSet, basename="transcript")

urlpatterns = [
    path("/", include(router.urls)),
]

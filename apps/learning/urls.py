from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.learning import views

router = DefaultRouter()
router.register("", views.LearningViewSet, basename="")

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.ai.translation import views

router = DefaultRouter()
router.register("translation", views.TranslationViewSet, basename=views.TranslationViewSet.basename)

urlpatterns = [
    path("", include(router.urls)),
]

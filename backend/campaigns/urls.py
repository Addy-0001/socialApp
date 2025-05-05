from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, CampaignCategoryViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'categories', CampaignCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

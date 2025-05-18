from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, CampaignCategoryViewSet, DonationViewSet


router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'categories', CampaignCategoryViewSet)
router.register(r'donations', DonationViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

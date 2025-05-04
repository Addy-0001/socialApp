from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Campaign
from .serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            # Only authenticated users can create/update campaigns
            return [IsAuthenticated()]
        if self.action == 'destroy':
            # Only admins can delete campaigns
            return [IsAdminUser()]
        return []

    def perform_create(self, serializer):
        # Set is_business based on user role
        serializer.save(
            created_by=self.request.user,
            is_business=self.request.user.role == 'BUSINESS'
        )

    def get_queryset(self):
        # Show only approved campaigns to non-admins
        if not self.request.user.is_staff:
            return Campaign.objects.filter(approved=True)
        return Campaign.objects.all()

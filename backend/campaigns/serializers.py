from rest_framework import serializers
from .models import Campaign, CampaignCategory, CampaignDonation
from user.serializers import CustomUserSerializer
from user.models import CustomUser


class CampaignCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCategory
        fields = "__all__"


class CampaignSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='created_by', write_only=True
    )
    category = CampaignCategorySerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'approved']


class CampaignDonationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    campaign = CampaignSerializer(read_only=True)
    campaign_id = serializers.PrimaryKeyRelatedField(
        queryset=Campaign.objects.all(), source='campaign', write_only=True
    )

    class Meta:
        model = CampaignDonation
        fields = "__all__"
        read_only_fields = ['id', 'donation_date']

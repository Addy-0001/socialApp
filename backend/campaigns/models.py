from django.db import models
from user.models import CustomUser


class CampaignCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Campaign Categories"
        ordering = ['name']


class Campaign(models.Model):
    TITLE_MAX_LENGTH = 255
    DESCRIPTION_MAX_LENGTH = 5000

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    category = models.ForeignKey(
        CampaignCategory, on_delete=models.CASCADE, related_name='campaigns')
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH)
    location = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to='campaigns/', blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    funding_goals = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)  # Funding goals
    is_featured = models.BooleanField(default=False)  # For featured campaigns
    is_active = models.BooleanField(default=True)  # For active campaigns
    is_completed = models.BooleanField(
        default=False)  # For completed campaigns

    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # For admin approval
    is_business = models.BooleanField(default=False)  # For business campaigns

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

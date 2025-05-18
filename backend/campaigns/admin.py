from django.contrib import admin
from .models import Campaign, CampaignCategory, CampaignDonation


class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'approved', 'is_business')
    search_fields = ('title', 'description')
    list_filter = ('approved', 'is_business', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('approved',)
    list_per_page = 20
    date_hierarchy = 'created_at'


class CampaignDonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'amount', 'donation_date')
    search_fields = ('campaign__title', 'user__username')
    list_filter = ('donation_date',)
    ordering = ('-donation_date',)
    list_per_page = 20
    date_hierarchy = 'donation_date'


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignCategory, CampaignCategoryAdmin)
admin.site.register(CampaignDonation, CampaignDonationAdmin)

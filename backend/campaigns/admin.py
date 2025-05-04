from django.contrib import admin
from .models import Campaign, CampaignCategory


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


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignCategory, CampaignCategoryAdmin)

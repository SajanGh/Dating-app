from django.contrib import admin
from user_profile.models import UserProfile, Heart


@admin.register(Heart)
class HeartAdmin(admin.ModelAdmin):
    list_display = ["sent_by", "received_by", "created_on"]


admin.site.register(UserProfile)

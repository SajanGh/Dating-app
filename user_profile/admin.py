from django.contrib import admin
from user_profile.models import UserProfile, Heart, UserDescription


@admin.register(Heart)
class HeartAdmin(admin.ModelAdmin):
    list_display = ["sent_by", "received_by", "created_on"]


@admin.register(UserDescription)
class UserDescriprionAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(UserProfile)

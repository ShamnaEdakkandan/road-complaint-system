# from django.contrib import admin
# from .models import Profile, Complaint

# admin.site.register(Profile)
# admin.site.register(Complaint)

# # Register your models here.

from django.contrib import admin
from .models import Profile, Complaint


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'role'
    ]


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'user',
        'location',
        'status',
        # 'assigned_to',
        # 'created_at'
    ]

    list_filter = [
        'status',
        'created_at'
    ]

    search_fields = [
        'title',
        'location',
        'user__username'
    ]
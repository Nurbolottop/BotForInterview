from django.contrib import admin
from .models import UserProfile, TelegramUser

# Register your models here.
admin.site.register(TelegramUser)


class UserProfileFilterAdmin(admin.ModelAdmin):
    list_filter = ('full_name','direction','user_id','status','total_score', )
    list_display = ('full_name','direction','user_id','status','total_score', )
    search_fields = ('full_name','direction','user_id','status','total_score', )
    
admin.site.register(UserProfile,UserProfileFilterAdmin)
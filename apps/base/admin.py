from django.contrib import admin
from apps.base.models import InterviewAnswer
# Register your models here.
class InterviewAnswerFilterAdmin(admin.ModelAdmin):
    list_filter = ('user_profile','question', 'answer', 'score',)
    list_display = ('user_profile','question','answer', 'score', )
    search_fields = ('user_profile','question', 'answer', 'score',)
    readonly_fields = ('user_profile', 'question', 'answer', )
    
admin.site.register(InterviewAnswer, InterviewAnswerFilterAdmin)

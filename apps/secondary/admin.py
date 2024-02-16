from django.contrib import admin

from apps.secondary import models 
# Register your models here.

class NapFilterAdmin(admin.ModelAdmin):
    list_filter = ('title', )
    list_display = ('title', )
    search_fields = ('title', )

class StatusFilterAdmin(admin.ModelAdmin):
    list_filter = ('title', )
    list_display = ('title', )
    search_fields = ('title', )

class QuestionInline(admin.TabularInline):
    model = models.QuestionAdd
    extra = 1
    
class QuestionFilterAdmin(admin.ModelAdmin):
    list_filter = ('direction', )
    list_display = ('direction', )
    search_fields = ('direction', )
    inlines = [QuestionInline]
    
admin.site.register(models.Question, QuestionFilterAdmin)
admin.site.register(models.Status, StatusFilterAdmin)
admin.site.register(models.Nap, NapFilterAdmin)
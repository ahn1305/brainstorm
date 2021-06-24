from django.contrib import admin
from django.db import models
from .models import user_interests,Code,Survey, Question, Option, Submission, Answer




class UserInterestsAdmin(admin.ModelAdmin):
    list_display = ['id','user','sports','music','science']
    list_display_links = ['id','user']
    fieldsets = [
        ('Username',{'fields':['user']}),
        ('Interests',{'fields':['sports','music','science']}),
        ]
    readonly_fields = ['user']




admin.site.register(user_interests,UserInterestsAdmin)
admin.site.register(Code)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)
from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','bio']
    list_display_links = ['id','user']
    fieldsets = [
        ('Username',{'fields':['user']}),
        ('ProfilePic',{'fields':['image']}),
        ('About',{'fields':['bio',]}),
        ('SocialMediaProfile',{'fields':['website_url','instagram_username','facebook_username','twitter_username','github_username','linkedin_username'],
        'classes':['collapse']}),
    ]


admin.site.register(Profile,ProfileAdmin)
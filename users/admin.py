from django.contrib import admin
from .models import Profile
import csv
from django.http import HttpResponse
# Register your models here.

def user_email(object):
  return object.user.email


class ProfileAdmin(admin.ModelAdmin):

    list_display = ['id','user',user_email,'bio']
    list_display_links = ['id','user']
    ordering = ['id']
    fieldsets = [
        ('Username',{'fields':['user']}),
        ('ProfilePic',{'fields':['image']}),
        ('About',{'fields':['bio',]}),
        ('SocialProfiles',{'fields':['website_url','instagram_username','facebook_username','twitter_username','github_username','linkedin_username'],
        'classes':['collapse']}),
    ]
    

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


# Adding export as csv option django admin: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html


admin.site.register(Profile,ProfileAdmin)
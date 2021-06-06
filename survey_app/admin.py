from django.contrib import admin
from .models import user_interests,Code,Survey, Question, Option, Submission, Answer


admin.site.register(user_interests)
admin.site.register(Code)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)
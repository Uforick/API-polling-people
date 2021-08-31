from django.contrib import admin

from .models import AnswerForChoice, Poll, Question

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(AnswerForChoice)

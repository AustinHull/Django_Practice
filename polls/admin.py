from django.contrib import admin

# Register your models here.
from .models import Question, EstimatedWaitTime

admin.site.register(Question)
admin.site.register(EstimatedWaitTime)

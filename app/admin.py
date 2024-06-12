from django.contrib import admin
from .models import Cohort, Topic, Message, Visibility, User

admin.site.register(User)
admin.site.register(Cohort)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Visibility)


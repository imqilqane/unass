from django.contrib import admin
from .models import User, user_profile

admin.site.register(User)
admin.site.register(user_profile)
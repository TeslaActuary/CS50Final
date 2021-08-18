from django.contrib import admin
from .models import User, Snake, Trivia

# Register your models here.
admin.site.register(User)
admin.site.register(Snake)
admin.site.register(Trivia)
from django.contrib import admin
from .models import User, Error, Solution, Match

# Register your models here.
admin.site.register(User)
admin.site.register(Error)
admin.site.register(Solution)
admin.site.register(Match)
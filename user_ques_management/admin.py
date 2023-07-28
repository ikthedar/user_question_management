from django.contrib import admin
from .models import UserProfile, Question, FavoriteQuestion, ReadQuestion

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(FavoriteQuestion)
admin.site.register(ReadQuestion)

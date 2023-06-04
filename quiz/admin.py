from django.contrib import admin
from .models import User, Quiz, Answers, UserHistory


class QuizId(admin.ModelAdmin):
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(User)
admin.site.register(Quiz, QuizId)
admin.site.register(Answers)
admin.site.register(UserHistory)

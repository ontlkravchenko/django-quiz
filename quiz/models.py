from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    score = models.IntegerField(
        blank=True,
        null=True,
        default=0
    )


class Quiz(models.Model):
    question = models.CharField(max_length=300)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.question}"


class Answers(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=69)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.quiz.id} - {self.answer} - {self.is_correct}"


class UserHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    answered = models.ManyToManyField(
        Quiz,
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return f"{self.user}'s history"

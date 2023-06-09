from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django.db import models
import random
from django.utils import timezone

class Question(models.Model):
       # id            = models.CharField(max_length=10, null=False, primary_key=True)
       question      = models.CharField(max_length=500, null=False)
       created_on    = models.DateTimeField(auto_now_add=True)
       def __str__(self):
              return str(self.question)


class Choice(models.Model):
       title         = models.CharField(max_length=50, null=False)
       isAnswer      = models.BooleanField(default=False)
       question      = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)

class Category(models.Model):
       list_subjects = (
              (1, "Math"),
              (2, "English"),
              (3, "Vietnamese"),
              (4, "Physics")
              )
       list_grades   = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12))
       list_levels   = ((1, 'Easy'), (2, 'Normal'), (3, 'Hard'))

       # id            = models.CharField(max_length=10, null=False, auto_created=True, primary_key=True)
       name          = models.CharField(max_length=50)
       grade         = models.IntegerField(choices=list_grades, default=1)
       level         = models.IntegerField(choices=list_levels, default=1)
       subject       = models.IntegerField(choices=list_subjects, default=1)
       questions     = models.ManyToManyField(Question, related_name="categories")

# class QuestionCategory(models.Model):
#        question      = models.ForeignKey(Question, on_delete=models.CASCADE)
#        category      = models.ForeignKey(Category, on_delete=models.CASCADE)


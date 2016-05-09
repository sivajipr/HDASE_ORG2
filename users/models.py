from django.db import models
from django.contrib.auth.models import User

# Create your models here


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    phone_number = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)


class Question(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=2000)

    def __unicode__(self):
        return '{0}'.format(self.question)


class Answered(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=20)


class Course(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0}'.format(self.name)


class AttendedCourse(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class CourseQuestion(models.Model):
    course = models.ForeignKey(Course)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

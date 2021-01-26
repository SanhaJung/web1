from django.db import models


class Error(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=225)
    message = models.TextField()
    code = models.TextField()
    status = models.BooleanField()
    description = models.TextField()


class User(models.Model):
    objects = models.Manager()
    user_name = models.CharField(max_length=20)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=100)
    user_validate = models.BooleanField(default=False)


class Match(models.Model):
    objects = models.Manager()
    error_id = models.IntegerField()
    user_id = models.IntegerField()


class Solution(models.Model):
    objects = models.Manager()
    solution_code = models.TextField()
    solution_description = models.TextField()
    user_id = models.IntegerField()
    error_id = models.IntegerField()
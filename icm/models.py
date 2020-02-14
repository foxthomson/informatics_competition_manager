# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    usertype = models.CharField(
        max_length=1,
        choices=(
            ('A', "Admin"),
            ('Q', "Question setter"),
            ('C', "Competitior")
        )
    )
    compname = models.CharField(max_length=64, null=True)

    # Link to user
    user = models.OneToOneField(User)

class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    timetorun = models.SmallIntegerField()
    author = models.CharField(User, default="admin", max_length=150)

class TestCase(models.Model):
    question = models.ForeignKey(Question)
    testinput = models.TextField()
    testoutput = models.TextField()
    weighting = models.SmallIntegerField()

class Competition(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    questions = models.ManyToManyField(Question)
    endtime = models.DateTimeField()
    scoringtype = models.CharField(
        max_length=1,
        choices=(
            ('=', "1 pass = 1 point"),
            ('%', "Percent passed"),
            ('s', "Sum of square of passes"),
            ('S', "Sum of square of percent passed"),
            ('1', "All passed = 1 point"),
        )
    )
    active = models.BooleanField()

class Submission(models.Model):
    user = models.ForeignKey(User)
    competition = models.ForeignKey(Competition)
    question = models.ForeignKey(Question)
    score = models.IntegerField()
    submission = models.FileField(upload_to="user_submissions", max_length=10240)

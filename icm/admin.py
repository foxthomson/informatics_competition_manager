# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Type
from .models import Question, TestCase
from .models import Competition, Submission

admin.site.register(Type)
admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(Competition)
admin.site.register(Submission)

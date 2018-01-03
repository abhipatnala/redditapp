# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Question,Comment

admin.site.register(Question)
admin.site.register(Comment)

# Register your models here.

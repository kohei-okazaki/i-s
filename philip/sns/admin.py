# -*- coding: utf-8 -*-
from django.contrib import admin
from sns.models import Message, Group, Friend, Good

# Register your models here.
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(Friend)
admin.site.register(Good)

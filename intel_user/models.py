# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    """
    用户信息
    """
    user = models.OneToOneField(User)
    iphone = models.CharField(max_length=11)

    class Meta:
        db_table = "user_info"

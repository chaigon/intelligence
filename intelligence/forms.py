# coding:utf-8

from django import forms


class BaseForm(forms.Form):
    """入口函数  跳转并执行action"""
    # user_id = forms.IntegerField(min_value=1, required=False)
    action = forms.CharField(max_length=60)

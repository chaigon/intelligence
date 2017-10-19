# coding:utf-8

from django import forms


class AnalysisForm(forms.Form):
    domain_ip = forms.CharField(max_length=64)

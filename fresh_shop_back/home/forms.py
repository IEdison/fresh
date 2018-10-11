
from django import forms


class UserLoginForm(forms.Form):

    username = forms.CharField(required=True,
                               error_messages={'required': '账号必填'})
    password = forms.CharField(required=True,
                               error_messages={'required': '密码必填'})


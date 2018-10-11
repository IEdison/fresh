
from django import forms

from users.models import User


class UserRegisterForm(forms.Form):
    """
    用户注册验证表单
    """
    user_name = forms.CharField(required=True, max_length=20, min_length=5,
                                error_messages={'required': '用户名必填',
                                                'max_length': '用户名不能超过20个字符',
                                                'min_length': '用户名不能少于5个字符'})
    pwd = forms.CharField(required=True, min_length=8, max_length=20,
                          error_messages={'required': '密码必填',
                                          'max_length': '密码长度不能超过20字符',
                                          'min_length': '密码长度不能短于5个字符'})
    cpwd = forms.CharField(required=True, min_length=8, max_length=20,
                          error_messages={'required': '确认密码必填',
                                          'max_length': '密码长度不能超过20字符',
                                          'min_length': '密码长度不能短于5个字符'})
    email = forms.CharField(required=True,
                            error_messages={'required': '邮箱必填'})
    allow = forms.BooleanField(required=True,
                               error_messages={'required': '请勾选协议'})

    def clean(self):
        username = self.cleaned_data.get('user_name')
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        # 校验用户名是否已经注册过
        user = User.objects.filter(username=username)
        # 如果user存在，说明该用户名已注册
        if user:
            raise forms.ValidationError({'user_name': '用户名已存在'})
        # 如果密码和确认密码不一致，提示密码错误
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})

        return self.cleaned_data


class UserLoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(required=True, max_length=20, min_length=5,
                                error_messages={'required': '用户名必填',
                                                'max_length': '用户名不能超过20个字符',
                                                'min_length': '用户名不能少于5个字符'})
    pwd = forms.CharField(required=True, min_length=8, max_length=20,
                          error_messages={'required': '密码必填',
                                          'max_length': '密码长度不能超过20字符',
                                          'min_length': '密码长度不能短于5个字符'})
    def clean_username(self):
        # 验证用户名是否注册过
        username=self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError({'username': '该用户没有注册，请去注册'})
        return username


class UserAddressForm(forms.Form):
    # 用户地址保存的表单验证
    signer_name = forms.CharField(required=True, error_messages={'required': '收件人必填'})
    address = forms.CharField(required=True, error_messages={'required': '详细地址必填'})
    signer_mobile = forms.CharField(required=True, error_messages={'required': '收件人手机号码必填'})
    signer_postcode = forms.CharField(required=True, error_messages={'required': '邮编必填'})

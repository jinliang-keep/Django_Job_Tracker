from django import forms
from django.contrib.auth.models import User
from .models import Job
import re

# 用户登录表单类
class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=150)
    password = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput)

    # 检查用户名是否已注册
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名未注册")
        
        return username

# 自定义一个用户注册表单类
class RegisterForm(forms.Form):
    email = forms.EmailField(label="邮箱", max_length=254)
    username = forms.CharField(
        label="用户名"
        , max_length=150
        # ,error_messages={
        #     "invalid": "请输入有效的邮箱地址",
        #     "required": "邮箱不能为空"}
    )
    password = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", max_length=128, widget=forms.PasswordInput)

    # 自定义验证函数，检查密码是否一致
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            self.add_error('password2', "两次输入的密码不一致")
            # raise forms.ValidationError("两次输入的密码不一致")
        
        #密码强度验证
        if password:
            if len(password) < 8:
                self.add_error('password', "密码长度至少为8位")
                # raise forms.ValidationError("密码长度不能少于8位")
            if not re.search(r'[A-Za-z]', password):
                self.add_error('password', "密码中必须包含字母")
                # raise forms.ValidationError("密码中必须包含字母")
            if not re.search(r'\d', password):
                self.add_error('password', "密码中必须包含数字")
                # raise forms.ValidationError("密码中必须包含数字")
        
        return cleaned_data
    
    # 检查邮箱是否存在
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已被注册")
        
        return email
    
    # 检查用户名是否已存在
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名已存在")
        
        return username

# 职位表单
class JobForm(forms.ModelForm):
    # status = forms.ChoiceField(
    #     widget=forms.Select(attrs={'class': 'form-select'})
    # )
    class Meta:
        model = Job
        fields = ['company', 'title', 'salary', 'location', 'status', 'note', 'date_applied', 'link']
        labels = {
            'company': '公司名称',
            'title': '职位名称',
            'salary': '薪资',
            'location': '工作地点',
            'status': '投递状态',
            'note': '备注',
            'date_applied': '投递日期',
            'link': '职位链接',
        }
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'id': 'company'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'id': 'salary'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'location'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'id': 'note'}),
            'date_applied': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'date_applied'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'id': 'link'}),
        }
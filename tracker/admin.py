from django.contrib import admin
from .models import Job

# Register your models here.
# 把模型注册到Django后台管理系统中
admin.site.register(Job)
from django.db import models
from django.contrib.auth.models import User

# # Create your models here.

# 职位类
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= "所属用户")
    company = models.CharField(max_length=100, verbose_name= "公司名称")
    title = models.CharField(max_length=100, verbose_name= "职位名称")
    salary = models.CharField(max_length=100, blank=True, verbose_name= "薪资")
    location = models.CharField(max_length=100, blank=True, verbose_name= "工作地点")
    status_choices = [
        ("not_applied", "未投递"),
        ("applied", "已投递"),
        ("interviewed", "已面试"),
        ("offer", "已拿offer"),
        ("rejected", "已拒绝"),
        ("fail", "未通过"),
        # ("waiting", "待定"),
    ]
    status = models.CharField(max_length=20, choices=status_choices,  default="not_applied", verbose_name="投递状态")
    note = models.TextField(blank=True, verbose_name= "备注")
    date_applied = models.DateField(blank=True, null=True, verbose_name= "投递日期")
    link = models.URLField(blank=True, verbose_name= "职位链接")

    def __str__(self):
        return f"{self.user} - {self.company} - {self.title} - {self.salary}"
    
    def status_badge(self):
        return {
            'not_applied': ('未投递', 'secondary'),
            'applied': ('已投递', 'primary'),
            'interviewed': ('已面试', 'primary'),
            'offer': ('已拿offer', 'success'),
            'rejected': ('已拒绝', 'danger'),
            'fail': ('未通过', 'danger'),
        }.get(self.status)

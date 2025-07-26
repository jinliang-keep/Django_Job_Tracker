from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm, LoginForm, JobForm

# 用于显示提示消息
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import make_password
from datetime import datetime

# 关键词搜索功能
from django.db.models import Q

# Create your views here.
# 1、首页
def home(request):
    return render(request, 'tracker/home.html')

# 2、登录
def login_view(request):
    
    if request.method == 'POST':
        # 1、将用户提交的数据传给表单
        form = LoginForm(request.POST)
        # 验证表单是否合法
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 检查用户名和密码是否正确
            user = authenticate(request, username=username, password=password)
            if user is not None: 
                login(request, user)
                messages.success(request, "您已成功登录！")
                return redirect('job_list')
            else:
                messages.error(request, "用户名或密码错误！")

    else:
        form = LoginForm()
    return render(request, 'tracker/login.html', {'form': form})

# 3、登出
@login_required # 只有登录用户才能登出
def logout_view(request):
    logout(request)
    messages.success(request, "您已成功登出。")
    return redirect('home')

# 4、注册
def register(request):
    
    if request.method == 'POST':
        # 将用户提交的数据传给表单
        form = RegisterForm(request.POST)

        if form.is_valid():
            
            # 提取数据
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            # 创建用户并保存
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # 自动登录新注册的用户
            login(request, user)

            # 显示成功消息
            messages.success(request, "注册成功，欢迎你，{}！".format(username))

            # 跳转到首页
            return redirect('home')
    
    else:
        form = RegisterForm()

    return render(request, 'tracker/register.html', {"form": form})

# 5、职位列表页面
@login_required
def job_list(request):

    # 获取关键词
    query = request.GET.get('q')
    no_result = False

    # 如果用户使用搜索功能
    if query:
        keywords = query.strip().split() # 拆分关键词
        
        base_filter = Q(user=request.user) # 只查当前登录用户的职位
        keyword_filter = Q()

        # 遍历关键字
        for word in keywords:
            keyword_filter |= (
                Q(company__icontains=word) | 
                Q(title__icontains=word) | 
                Q(salary__icontains=word) | 
                Q(location__icontains=word)
            )
        
        final_filter = base_filter & keyword_filter
        jobs = Job.objects.filter(final_filter).order_by('-date_applied')

        # jobs = Job.objects.filter(
        #     Q(user=request.user) & (
        #         Q(company__icontains=query) | 
        #         Q(title__icontains=query) | 
        #         Q(salary__icontains=query) | 
        #         Q(location__icontains=query)
        #     )        
        # ).order_by('-date_applied')

        # 如果搜索无结果
        if not jobs.exists():
            no_result = True  

    # 展示职位列表
    else:
        jobs = Job.objects.filter(user=request.user).order_by('-date_applied')

    # 用户提交表单，添加、编辑职位
    if request.method == 'POST':
        job_id = request.POST.get('job_id')

        # 编辑职位
        if job_id:
            job = get_object_or_404(Job, id=job_id, user=request.user)
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, "职位更新成功！")
                return redirect('job_list')

        # 新增职位
        else:
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.user = request.user
                job.save()
                messages.success(request, "职位添加成功！")
                return redirect('job_list') # 刷新页面
            else:
                messages.error(request, "请检查输入内容。")

    else:
        form = JobForm()

    return render(request, 'tracker/job_list.html', {
        'jobs': jobs,
        'form': form,
        'no_result': no_result,
        'timestamp': datetime.now().timestamp(), })

# 6、删除职位
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)

    job.delete()

    return redirect('job_list')

# 7、编辑职位
# @login_required
# def edit_job(request, job_id):
#     job = get_object_or_404(Job, id=job_id, user=request.user)

#     if request.method == 'POST':
#         form = JobForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             return redirect('job_list')
#     else:
#         form = JobForm(instance=job)
    
#     return render(request, 'tracker/edit_job.html', {'form': form})


# 返回职位详情
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)

    data = {
        'job_id': job.id,
        'company': job.company,
        'title': job.title,
        'salary': job.salary,
        'location': job.location,
        'status': job.status,
        'note': job.note,
        'date_applied': job.date_applied.strftime('%Y-%m-%d') if job.date_applied else '',
        'link': job.link,
    }

    return JsonResponse(data)
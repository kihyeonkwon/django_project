from http import HTTPStatus
from operator import ge
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login as loginsession

# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method =='POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        passwordcheck = request.POST.get('passwordcheck', None)

        if password != passwordcheck:
            return render(request, 'user/signup.html')
        else:
            #에러처리
            User.objects.create_user(username=username, password=password)
            # 안되는 코드
            # user = User()
            # user.password = password
            # return redirect('/sign-in') # 회원가입이 완료되었으므로 로그인 페이지로 이동
            return render(request, 'login.html')
            return HttpResponse("Good")
    else:
        # 안좋은 코드
        return HttpResponse("Bad Method")

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method =='POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            print(user)
            loginsession(request, user)
            return redirect('users:user')
        else:
            return HttpResponse("로그인 실패")

def user(request):
    return HttpResponse(request.user)


def profile(request, username):
    # user = User.objects.get(username = username)
    user = get_object_or_404(User, username=username)
    context = {
        "user":user,
        "me":request.user
    }
    return render(request, 'profile.html', context)
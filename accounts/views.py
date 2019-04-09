from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import UserCustomChangeForm

# Create your views here.

def signup(request):
    if request.user.is_authenticated:           # 로그인 상태인지 확인. 로그인상태하면 인덱스 페이지로 보낸다.
        return redirect('boards:index')
        
    if request.method == 'POST':                    # create 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                      # 1. 
            auth_login(request, user)               # 2. 회원가입하자마자 로그인될 수 있도록
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    if request.user.is_authenticated:           # 로그인상태에서 로그인하면 안되므로 필요
        return redirect('boards:index')
    
    if request.method == 'POST':
         form = AuthenticationForm(request, request.POST)
         if form.is_valid():
             auth_login(request, form.get_user())
             return redirect('boards:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('boards:index')
    
    
# 회원 탈퇴
def delete(request):        
    user = request.user
    if request.method == 'POST':
        user.delete()
    return redirect('boards:index')
    
def edit(request):
    if request.method == 'POST':
        # 수정 로직 진행
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {'form': form,}
    return render(request, 'accounts/edit.html', context)
    
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)   # 인자 순서 유의
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # 현재 유저가 로그아웃 되는 것을 막는다
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form,}
    return render(request, 'accounts/change_password.html', context)
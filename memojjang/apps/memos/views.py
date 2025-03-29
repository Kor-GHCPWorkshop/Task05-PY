from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from ..users.models import User
from .models import Memo
from ...forms import MemoForm, UserRegistrationForm


def home(request):
    """홈페이지 뷰"""
    return render(request, "home.html")


@login_required
def memo_list(request):
    """메모 목록 뷰"""
    memos = Memo.objects.filter(user=request.user)
    return render(request, "memos/memo_list.html", {"memos": memos})


@login_required
def memo_create(request):
    """메모 생성 뷰"""
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect("memo_list")
    else:
        form = MemoForm()
    return render(request, "memos/memo_form.html", {"form": form})


@login_required
def memo_detail(request, pk):
    """메모 상세 뷰"""
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    return render(request, "memos/memo_detail.html", {"memo": memo})


@login_required
def memo_edit(request, pk):
    """메모 수정 뷰"""
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect("memo_detail", pk=pk)
    else:
        form = MemoForm(instance=memo)
    return render(request, "memos/memo_form.html", {"form": form})


@login_required
def memo_delete(request, pk):
    """메모 삭제 뷰"""
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        memo.delete()
        return redirect("memo_list")
    return render(request, "memos/memo_confirm_delete.html", {"memo": memo})


def login_view(request):
    """로그인 뷰"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("memo_list")
        else:
            messages.error(request, "로그인에 실패했습니다.")
    return render(request, "users/login.html")


@login_required
def logout_view(request):
    """로그아웃 뷰"""
    logout(request)
    return redirect("home")


def register(request):
    """회원가입 뷰"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("memo_list")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})
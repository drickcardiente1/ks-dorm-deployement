from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('room_status_all_admin')
            elif user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, "You may have entered an invalid username or password. Try again...")
                messages.success(request, "Your account may be deactivated by the admin...")
                return redirect('login')
        except Exception as e:
            messages.error(request, "An error occurred while trying to log in. Please try again later.")
            return render(request, 'user/error_page.html', {'error': str(e)})
    else:
        return render(request, 'authentication/login.html', {})


def login_modal(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('room_status_all_admin')
            elif user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, "You may have entered an invalid username or password. Try again...")
                messages.success(request, "Your account may be deactivated by the admin...")
                return redirect('home')
        except Exception as e:
            messages.error(request, "An error occurred while trying to log in. Please try again later.")
            return render(request, 'user/error_page.html', {'error': str(e)})
    else:
        return render(request, 'authentication/login.html', {})


def logout_user(request):
    messages.success(request, "You Are Now Logged Out...")
    logout(request)
    return redirect('home')


from users.models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreateForm, UserLoginForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


def landing_page(request):
    return render(request, "landing.html")

class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form':create_form
        }
        return render(request, 'users/register.html', context=context)
    
    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
        else:
            context = {
                'form':create_form
            }
            return render(request, 'users/register.html', context=context)
            

        return redirect('users:login')


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {"login_form":login_form})
    
    def post(self, request):
        # Deeper validate qilish uchun AuthenticationForm()
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, "You have successfully logged in!")
            return redirect("books:list")
        else:
            return render(request, 'users/login.html', {'login_form':login_form})
        

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "users/profile.html", {"user":request.user})
    
        # if not request.user.is_authenticated:
        #     return redirect("users:login")
        # Shu ishni tayyor mixin orqali qilish mumkin
        

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have succesfully logged out!")
        return redirect("users:landing_page")
    

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user) # Qaysi userni change qilmoqchi ekani
        return render(request, "users/profile_edit.html", {'form':user_update_form})
    
    def post(self, request):
        user_update_form = UserUpdateForm(instance=request.user, data=request.POST)
        
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully changed credentials!")
        
            return redirect("users:profile")
        
        else:
            return render(request, "users/profile_edit.html", {"form":user_update_form})
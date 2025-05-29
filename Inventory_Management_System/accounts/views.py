from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import EmployeeRegistrationForm
from django.contrib import messages
from django.shortcuts import render
from django.db import connection

User = get_user_model()
def home(request):
    return render(request, "accounts/home.html")
class LoginView(AuthLoginView):
    template_name = "accounts/login.html"
    next_page= "home"

class LogoutView(AuthLogoutView):
    next_page = "login"

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/dashboard.html")

class RegisterEmployeeView(LoginRequiredMixin, View):
    template_name = "accounts/register_employee.html"
    def get(self, request):
        form = EmployeeRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "employee"
            user.set_password(form.cleaned_data["password"])
            user.save()
            print(user.role)
            messages.success(request, f"Employee '{user.username}' registered successfully.")
            return redirect("dashboard")
        return render(request, self.template_name, {"form": form})
    
    def dispatch(self, request, *args, **kwargs):
        if  request.user.role == "employee"  and not request.user.is_superuser :
            messages.warning(request, "You do not have permission to add employees.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)
    


    

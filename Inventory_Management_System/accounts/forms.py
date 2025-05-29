from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        help_text="Password must be at least 8 characters long, contain both letters and numbers, and have no spaces.",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )
    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r"^[A-Za-z]{4,20}$", username):
            raise ValidationError("Username must contain only letters and be 4-20 characters long.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValidationError("Enter a valid email address.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            raise ValidationError("Password must contain at least one letter, one number, and be at least 8 characters long.")
        return password

    def clean_confirm_password(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password 

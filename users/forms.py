from django import forms
from users.models import CustomUser

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password",)

    def save(self, commit=True):
        # Override qilishdan oldingi .save() ni super() classi orqali chaqirib user saqlab oldik
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)

    """Quyidagi kabi clean() override qilish common bolgani uchun, Djangoda AuthenticationForm() ishlab chiqilgan"""
    # def clean(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("profile_picture","username", "first_name", "last_name", "email",)
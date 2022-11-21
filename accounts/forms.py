from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import User


class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', )


class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
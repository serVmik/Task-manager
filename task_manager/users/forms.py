from django.contrib.auth.forms import UserCreationForm

from task_manager.users.models import AppUser


class UserCreateForm(UserCreationForm):

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')


class UserUpdateForm(UserCreateForm):

    def clean_username(self):
        return self.cleaned_data.get("username")

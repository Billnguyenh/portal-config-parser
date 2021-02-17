from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.forms import ModelForm


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].lable = 'Email Address'


class ProfileEditForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

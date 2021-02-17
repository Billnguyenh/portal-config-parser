from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from accounts import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

class ProfileEditView(UpdateView):
    form_class = forms.ProfileEditForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


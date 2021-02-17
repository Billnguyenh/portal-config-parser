from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def home_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('win_parser:upload'))
    else:
        return HttpResponseRedirect(reverse('accounts:login'))
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView, ListView

from win_parser.models import WindowsConfigFile, WindowsConfig
from win_parser.forms import WindowsConfigFileForm

from win_parser.winsys import WinSys

import re, json

class FileUploadView(FormView, ListView, LoginRequiredMixin):
    model = WindowsConfigFile
    form_class = WindowsConfigFileForm
    context_object_name = 'windowsconfigfiles'
    template_name = 'win_parser/upload.html'
    success_url = reverse_lazy('win_parser:upload')

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save(commit=False)
        if self.request.FILES:
            for config in self.request.FILES.getlist('config_file'):
                obj = self.model.objects.create(config_file=config, user=form.instance.user)
        return super().form_valid(form)

    def get_queryset(self):
        user = self.request.user
        return WindowsConfigFile.objects.filter(user=user)

# from django.core.files.storage import FileSystemStorage
# #Function-based view with no model example
# def upload(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['configs']
#         print(uploaded_file.name)
#         fs = FileSystemStorage()
#         fs.save(uploaded_file.name, uploaded_file)
#     return render(request, 'win_parser/upload.html')

# from .forms import BookForm
# #Function-based view with model example
# def book_list(request):
#     return render(request, 'win_parser/book_list.html')
    
# def upload_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('win_parser:book_list')
#     else:
#         form = BookForm()
#     return render(request, 'win_parser/upload_book.html', {
#         'form':form
#     })

class ReportView(ListView, LoginRequiredMixin):
    model = WindowsConfig
    context_object_name = 'windowsconfigs'
    template_name = 'win_parser/reports.html'

    
def delete_config_file(request, pk):
    if request.method == 'POST':
        config_file = WindowsConfigFile.objects.get(pk=pk)
        config_file.delete()
    return redirect('win_parser:upload')

def parse_configs(request):
    WindowsConfig.objects.all().delete()
    if request.method == 'POST':
        for config_model in WindowsConfigFile.objects.all():
            file_path = config_model.config_file.path
            print("Parsing " + file_path)
            if file_path.endswith('.txt'):
                config_file = open(file_path, 'r', errors="ignore")
                file_contents = config_file.readlines()
                create_config_model(WinSys(file_contents, 'script'))
                config_file.close()
    return redirect('win_parser:reports')

def convertToJson(attributes):
    return json.dumps(attributes, indent=4)

def decodeJson(json_test):
    json_dec = json.decoder.JSONDecoder()
    return json_dec.decode(json_test)

def create_config_model(winsys):
    windows_config = WindowsConfig(
        hostname = winsys.getHostname(),
        operating_system = winsys.getOs(),
        hardware = winsys.getHardware(),
        domain_name = winsys.getDomainName(),

        time_source = winsys.getTimeSource(),
        time_peer = winsys.getTimePeer(),
        
        screen_saver_timeout = winsys.getScreenSaverTimeout(),
        rdp_security_level = winsys.getRdpSecurityLevel(),

        network_adapters = convertToJson(winsys.getNetworkAdapters()),
        network_wlans = convertToJson(winsys.getNetworkWlans()),
        users = convertToJson(winsys.getUsers()),
        admins = convertToJson(winsys.getAdmins()),
        default_users = convertToJson(winsys.getDefaultUsers()),
        programs = convertToJson(winsys.getPrograms()),
        services = convertToJson(winsys.getServices()),
        listening_ports = convertToJson(winsys.getListeningPorts()),
        gpresult = convertToJson(winsys.getGpresult()),
        password_policies = convertToJson(winsys.getPasswordPolicies()),
        account_lockout_policies = convertToJson(winsys.getAccountLockoutPolicies()),
        audit_policies = convertToJson(winsys.getAuditPolicies()),
        privilege_rights = convertToJson(winsys.getPrivilegeRights()),
        registry_values = convertToJson(winsys.getRegistryValues()),
        security_updates = convertToJson(winsys.getSecurityUpdates()),
        inactive_users = convertToJson(winsys.getInactiveUsers()),
        disabled_users = convertToJson(winsys.getDisabledUsers()),
        all_users = convertToJson(winsys.getAllUsers()),
        )
    windows_config.save()
    



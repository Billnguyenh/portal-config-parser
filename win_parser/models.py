from django.db import models

import os, re, json

from django.core.validators import FileExtensionValidator

from django.contrib.auth import get_user_model
User = get_user_model()

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class WindowsConfigFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    config_file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.config_file.name

    def filename(self):
        return os.path.basename(self.config_file.name)

    def delete(self, *args, **kwargs):
        self.config_file.delete() #Looks like FileField knows this means to delete actual file
        super().delete(*args, **kwargs)
        
class WindowsConfig(models.Model):
    hostname = models.CharField(blank=True, max_length=128)
    operating_system = models.CharField(blank=True, max_length=128)
    hardware = models.CharField(blank=True, max_length=128)
    domain_name = models.CharField(blank=True, max_length=128)

    time_source = models.CharField(blank=True, max_length=128)
    time_peer = models.CharField(blank=True, max_length=128)

    screen_saver_timeout = models.CharField(blank=True, max_length=128)
    rdp_security_level = models.CharField(blank=True, max_length=128)
    
    #All fields below are JSON-serialized. Use jsonDecode filter/template to retrieve in List/Dict form for reporting
    network_adapters = models.TextField(blank=True)
    network_wlans = models.TextField(blank=True)
    users = models.TextField(blank=True)
    admins = models.TextField(blank=True)
    default_users = models.TextField(blank=True)
    programs = models.TextField(blank=True)
    services = models.TextField(blank=True)
    listening_ports = models.TextField(blank=True)
    gpresult = models.TextField(blank=True)
    password_policies = models.TextField(blank=True)
    account_lockout_policies = models.TextField(blank=True)
    audit_policies = models.TextField(blank=True)
    privilege_rights = models.TextField(blank=True)
    registry_values = models.TextField(blank=True)
    security_updates = models.TextField(blank=True)
    inactive_users = models.TextField(blank=True)
    disabled_users = models.TextField(blank=True)
    all_users = models.TextField(blank=True)
    
    
    def __str__(self):
        return self.hostname





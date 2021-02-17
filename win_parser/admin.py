from django.contrib import admin
from win_parser.models import WindowsConfigFile, WindowsConfig

admin.site.register(WindowsConfigFile)
admin.site.register(WindowsConfig)


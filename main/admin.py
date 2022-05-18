from django.contrib import admin

from .models import Crime, Date, Location

admin.site.register(Crime)
admin.site.register(Date)
admin.site.register(Location)

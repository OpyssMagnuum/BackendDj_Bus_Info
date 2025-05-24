from django.contrib import admin
from main.models import Bus, Route, LongRouteName
# Register your models here.

admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(LongRouteName)

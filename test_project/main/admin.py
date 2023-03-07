from django.contrib import admin

from .models import JsonInputDate


class JsonInputDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date')


admin.site.register(JsonInputDate, JsonInputDateAdmin)

from django.contrib import admin
from crimeapp import models


class TaskHistoryAdminModel(admin.ModelAdmin):
    list_display = ("name",)
    class Meta:
        models.TaskHistory

class CrimesAdminModel(admin.ModelAdmin):
    list_display = ("date", "time", "first_name", "surname", "offense", "location")
    class Meta:
        models.Crimes

admin.site.register(models.TaskHistory, TaskHistoryAdminModel)
admin.site.register(models.Crimes, CrimesAdminModel)

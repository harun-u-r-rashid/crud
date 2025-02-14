from django.contrib import admin


from . import models

class AdminUser(admin.ModelAdmin):
        list_display = ["phone", "username", "id"]
        search_fields = ["phone"]
        list_filter = ["phone", "id"]


admin.site.register(models.User, AdminUser)
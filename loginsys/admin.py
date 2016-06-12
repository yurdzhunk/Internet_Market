from django.contrib import admin
from loginsys.models import User_Email

# Register your models here.

class EmailAdmin(admin.ModelAdmin):
    fields = ['emails_username', 'email', 'adress_of_user']
    list_filter = ['email']


admin.site.register(User_Email, EmailAdmin)
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets += (
    ("Phone number Auth", {'fields':('Phone',)}),

)
admin.site.register(User, UserAdmin)


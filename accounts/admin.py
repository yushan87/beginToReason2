"""
This module registers the models we created for the "accounts" application. After registering
the model, the data will be accessible through Django's admin functionality.
"""
from django.contrib import admin
from .models import UserInformation


class UserInformationAdmin(admin.ModelAdmin):
    """
    This class contains rendering details for the UserInformation table
    """
    model = UserInformation
    list_display = ('get_user_email', 'user_nickname', 'user_school', 'user_class')     # Fields to be shown initially

    def get_user_email(self, obj):
        """function get_user_email is an helper function to retrieve the email associated with the user

            Returns:
                str: user email
        """
        return obj.user.email

    get_user_email.short_description = 'User Email'  # Renames column head


# Register your models here.
admin.site.register(UserInformation, UserInformationAdmin)

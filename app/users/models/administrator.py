from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Administrator(CreatedModified):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='administrator_profile')

    def __str__(self):
        return self.user.email

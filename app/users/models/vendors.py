from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Vendors(CreatedModified):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='vendors_profile')

    def __str__(self):
        return self.user.email
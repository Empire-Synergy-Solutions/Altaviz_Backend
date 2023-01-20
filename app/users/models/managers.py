from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Managers(CreatedModified):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='managers_profile')
    vendors = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='vendors_managers')

    def __str__(self):
        return self.user.email
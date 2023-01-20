from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Attendants(CreatedModified):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='attendants_profile')
    vendors = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='vendors_attendants')

    def __str__(self):
        return self.user.email
from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Customers(CreatedModified):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='Customers_profile')

    def __str__(self):
        return self.user.email

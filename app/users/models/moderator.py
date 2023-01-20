from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Moderator(CreatedModified):
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='sponsored_moderators')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='moderator_profile')

    def __str__(self):
        return self.user.email

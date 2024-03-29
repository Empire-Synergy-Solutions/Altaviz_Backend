import uuid
from django.conf import settings
from django.db import models
from general.created_modified import CreatedModified


class Invitation(CreatedModified):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='sent_invitations')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='received_invitations')
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        default_related_name = 'invitations'

    def __str__(self):
        return f'{self.code}'

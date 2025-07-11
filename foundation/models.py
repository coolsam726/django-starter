from django.contrib.auth import get_user_model
from typing import Type

from django.contrib.auth.models import AbstractUser
from django.db import models

from foundation import helpers
from foundation.threadinglocals import get_current_user

# Abstract base model for common fields

BaseUser = get_user_model()
class BaseModel(models.Model):
    code = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    created_by = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name='%(class)s_created',
        blank=True, null=True
    )
    updated_by = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name='%(class)s_updated',
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    PREFIX = None # To be set in subclasses

    def _generate_code_prefix(self):
        return ''.join([c for c in self.__class__.__name__ if c.isupper()])
    def _get_prefix(self):
        return self.PREFIX or self._generate_code_prefix()

    def save(self, *args, **kwargs):
        current_user: Type[BaseUser] = get_current_user()
        if not self.code:
            self.code = helpers.generate_code(self) # This will also set the ID if it is not set.
        if not self.name:
            self.name = self.code
        if not self.created_by:
            self.created_by = current_user or None
        # Always set updated by
        self.updated_by = current_user or None
        super().save(*args, **kwargs)
    class Meta:
        abstract = True

class Team(BaseModel):
    """
    Represents a team in the system.
    """
    PREFIX = 'TM'
    description = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name
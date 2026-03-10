from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    level = models.CharField(max_length=100, blank=True)  # e.g. Senior, Junior
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.level})"

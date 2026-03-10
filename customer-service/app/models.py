from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.name


class FullName(models.Model):
    customer = models.OneToOneField(Customer, related_name="fullname", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    class Meta:
        app_label = "app"

    def __str__(self) -> str:
        return self.full_name


class Address(models.Model):
    customer = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.line1}, {self.city or ''}".strip(", ")
from django.db import models


class Account(models.Model):
    account_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    pin = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.name} ({self.account_number})"


# Create your models here.

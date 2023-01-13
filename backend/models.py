from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

PHONE_NUMBER_REGEX = RegexValidator(regex="^(\+\d{2})?\d{10}", message="Phone number is in a wrong format.")

class Partner(models.Model):
    first_name = models.CharField(blank=True, null=True, max_length=256)
    middle_name = models.CharField(blank=True, null=True, max_length=256)
    last_name = models.CharField(blank=True, null=True, max_length=256)

    mobile_number = models.CharField(blank=True, null=True, max_length=10,
                                    validators=[PHONE_NUMBER_REGEX])

    email_address = models.EmailField(primary_key=True)

    # Date format is YYYY-MM-DD
    date_of_birth = models.DateField(blank=True, null=True)
    partner_id = models.CharField(blank=True, null=True, max_length=12)

class Login(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    password_hash = models.CharField(null=True, blank=True, max_length=32)

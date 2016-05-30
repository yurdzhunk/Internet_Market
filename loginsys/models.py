from __future__ import unicode_literals
from validate_email import validate_email
from django.db import models


# Create your models here.

class User_Email(models.Model):

    class Meta:
        db_table = 'user_email'

    email = models.EmailField(default='test@gmail.com')
    emails_username = models.CharField(max_length=200)

    def email_is_valid(self):
        if validate_email(self.email):
            return True

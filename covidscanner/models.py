from django.db import models

# Create your models here.

class Passports(models.Model):
    passports = models.FileField(upload_to ='media/passports')
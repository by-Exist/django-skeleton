from django.db import models

# Create your models here.
class Example(models.Model):
    title = models.CharField("Title", max_length=12)

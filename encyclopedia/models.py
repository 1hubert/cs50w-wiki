from django.db import models

# Create your models here.
class Entry(models.Model):
    entry_title = models.CharField(max_length=100)
    entry_content = models.TextField(max_length=9000)
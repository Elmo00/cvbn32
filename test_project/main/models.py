from django.db import models


class JsonInputDate(models.Model):
    name = models.CharField(max_length=49)
    date = models.DateTimeField()

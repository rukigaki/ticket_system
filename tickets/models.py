from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


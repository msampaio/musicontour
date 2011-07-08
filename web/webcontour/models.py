from django.db import models

class Contour(models.Model):
    cps = models.CharField(max_length=100)

from django.db import models

OP_CHOICES = (('retrograde', 'Retrograde'), ('inversion', 'Inversion'),
              ('prime_form_sampaio', 'Prime form Sampaio'),
              ('prime_form_marvin_laprade', 'Prime form ML'),
              ('translate', 'Normal form'), ('all', 'All operations'))

class Contour(models.Model):
    cps = models.CharField(max_length=100)
    operation = models.CharField(max_length=30, choices=OP_CHOICES)


from django.db import models


class Contour(models.Model):

    OP_CHOICES = (('all', 'All operations'), ('translation', 'Normal form'),
                  ('prime_form_sampaio', 'Prime form Sampaio'),
                  ('prime_form_marvin_laprade', 'Prime form ML'),
                  ('retrograde', 'Retrograde'),
                  ('inversion', 'Inversion'))

    cps = models.CharField(max_length=100, default='0 2 1 3 4 5')
    operation = models.CharField(max_length=30, choices=OP_CHOICES, default='all')


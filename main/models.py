from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
 
class PageView(models.Model):
    class PageChoices(models.TextChoices):
        INDEX = 'index', 'Index'
        SI = 'si', 'SI'
        ISI = 'isi', 'ISI'
        DETAILS = 'details', 'Details' 
    student_id = models.CharField(max_length=8,null=True,blank=True)
    page = models.CharField(max_length=20, choices=PageChoices.choices)
    date_time = models.DateTimeField(default=timezone.now)


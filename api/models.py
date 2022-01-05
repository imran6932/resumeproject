
from django.db import models
from django.db.models.fields import FloatField

# Create your models here.

class my_input(models.Model):
    upload_file = models.FileField(upload_to='my_files')

    '''def __str__(self):
        return self.upload_file'''
    
     
    
     

# Create your models here
from django.db import models


#class Person(models.Model):
  #  first_name = models.CharField(max_length=30)
  #  last_name = models.CharField(max_length=30)
  #  def __str__(self):
  #     return self.first_name, self.last_name

class blogurls(models.Model):
  website=models.TextField(max_length=9000)
  numurls=models.IntegerField(0)
  def __str__(self):
        return self.website




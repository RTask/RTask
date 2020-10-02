from django.db import models

# Create your models here.
class Ticket (models.Model):
    Title = models.CharField(max_length=30,blank=False)
    Description =models.CharField(max_length=250,blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.Title,self.CreatedDate
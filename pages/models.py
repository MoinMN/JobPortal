from django.db import models

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
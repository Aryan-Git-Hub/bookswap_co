from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Book(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book')
    state = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    book_name = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    desc = models.CharField(max_length=300, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    publication = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, blank=True)
    pages = models.IntegerField(default=0, null=True)
    photo = models.ImageField(upload_to='books/', blank=True)

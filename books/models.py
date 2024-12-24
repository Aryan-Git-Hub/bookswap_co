from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Book(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book')
    state = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    colony = models.CharField(max_length=70)
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, default="Add Description")
    edition = models.CharField(max_length=50, default="Write Edition of Book")
    publication = models.CharField(max_length=100, default="Write Publication")
    category = models.CharField(max_length=50)
    pages = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='books')

    def save(self):
        print(self.photo.path)
        return super().save()
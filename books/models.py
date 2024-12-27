from django.db import models
from accounts.models import CustomUser
# to change dimentions of image
from PIL import Image


def resize_img(img_path, output_size):
    img = Image.open(img_path)
    img.thumbnail(output_size)
    background = Image.new('RGB', output_size, (255, 255, 255))  # Transparent background
    offset = ((output_size[0] - img.size[0]) // 2, (output_size[1] - img.size[1]) // 2)
    background.paste(img, offset)
    img = background
    img.save(img_path, format='JPEG', quality=95)


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
    pages = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='books/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 330) # (width, height=1.1*width)
            resize_img(self.photo.path, output_size)
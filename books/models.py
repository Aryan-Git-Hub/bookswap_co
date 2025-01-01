from django.db import models
from accounts.models import CustomUser
# for managing images
from django.conf import settings
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


base_path = str(settings.BASE_DIR)
def del_img(file_path):
    import os
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print('file does not delete because of', e)


# Create your models here.
class Book(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book')
    book_name = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    desc = models.CharField(max_length=300, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    publication = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, blank=True)
    pages = models.IntegerField(blank=True)
    price = models.IntegerField(blank=True)
    selected_address_id = models.IntegerField()

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            del_img(img.image.path)
        super().delete(*args, **kwargs)

class ImageModel(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models. ImageField (upload_to="books", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        w = 300
        h = 330 # h = 1.1*w
        if img.height > h or img.width > w:
            output_size = (w, h) # (width, height)
            resize_img(self.image.path, output_size)


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")
    books = models.JSONField(default=dict, blank=True)
    cart_val = models.IntegerField(default=0, blank=True)
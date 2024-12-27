from django.db import models
from django.contrib.auth.models import AbstractUser
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
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=150, unique=True)
    photo = models.ImageField(upload_to='user_photos', default='default_user_photo.png')
    mobile = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email


    # To saving image in a particular dimentions
    def save(self, *args, **kwargs):
        try:
            self_user = CustomUser.objects.get(id=self.id)
            if self_user.photo.path!=base_path+'/media/default_user_photo.png' and self.photo!=self_user.photo:
                # to remove previous images
                import os
                os.remove(self_user.photo.path)
        except:
            pass
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            resize_img(self.photo.path, output_size)

    def delete(self, *args, **kwargs):
        self_user_photo_path = self.photo.path
        super().delete(*args, **kwargs)
        if self_user_photo_path!=base_path+'/media/default_user_photo.png':
            del_img(self_user_photo_path)
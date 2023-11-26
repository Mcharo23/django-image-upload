from django.db import models
import uuid

# Create your models here.


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return '/'.join(['images', filename])


class UploadImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to)

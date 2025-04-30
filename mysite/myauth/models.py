from django.db import models
from django.contrib.auth.models import User


def gen_image_path(instance: 'Profile', filename: str):
    return 'users/user_{pk}/{filename}'.format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=gen_image_path)





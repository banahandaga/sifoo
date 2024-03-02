from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from uuid import uuid4
import os


def path_image(instance, filename):
    upload_to = 'images/profile'
    ext = filename.split('.')[-1]
    hex = '{}'.format(uuid4().hex)
    filename = '%s.%s' % (hex, ext)
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    nip           = models.CharField(max_length=20, null=True, blank=True)
    nidn          = models.CharField(max_length=50, null=True, blank=True)
    surelluar     = models.CharField(max_length=100, null=True, blank=True)
    nomorhp       = models.CharField(max_length=15, null=True, blank=True)
    is_dosen      = models.IntegerField(null=True, blank=True)
    home_id       = models.CharField(max_length=20, null=True, blank=True)
    homebase      = models.CharField(max_length=255, null=True, blank=True)
    image         = models.ImageField(null=True, blank=True, upload_to=path_image)
    otp           = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        txt = '{\n'
        txt += 'USERNAME \t: ' + str(self.user.username) + ',\n'
        txt += 'NIP \t: ' + str(self.nip) + ',\n'
        txt += 'NIDN \t: ' + str(self.nidn) + ',\n'
        txt += 'SURELLUAR \t: ' + str(self.surelluar) + ',\n'
        txt += 'NOMORHP \t: ' + str(self.nomorhp) + ',\n'
        txt += 'IS_DOSEN \t: ' + str(self.is_dosen) + ',\n'
        txt += 'HOME_ID \t: ' + str(self.home_id) + ',\n'
        txt += 'HOMEBASE \t: ' + str(self.homebase) + ',\n'
        txt += 'IMAGE \t: ' + str(self.image) + ',\n'
        txt += 'OTP \t: ' + str(self.otp) + ',\n'
        txt += '}\n'
        return txt


    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return os.path.join(settings.STATIC_URL, 'images/profile/default.png')


    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except: pass
        super(Profile, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Profile, self).delete(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
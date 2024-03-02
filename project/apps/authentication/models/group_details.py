from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


class GroupDetails(models.Model):
    group           = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='groupdetails', primary_key=True)
    alias           = models.CharField(max_length=100, null=True)
    description     = models.TextField(null=True)
    created         = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        txt = '{\n'
        txt += 'GROUP_NAME \t: ' + str(self.group.name) + ',\n'
        txt += 'ALIAS \t: ' + str(self.alias) + ',\n'
        txt += 'DESCRIPTION \t: ' + str(self.description) + ',\n'
        txt += 'CREATED \t: ' + str(self.created) + ',\n'
        txt += '}\n'
        return txt


@receiver(post_save, sender=Group)
def create_group_details(sender, instance, created, **kwargs):
    if created:
        GroupDetails.objects.create(group=instance)


@receiver(post_save, sender=Group)
def save_group_details(sender, instance, **kwargs):
    instance.groupdetails.save()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile

@receiver(post_save, sender=User)
def assign_driver_role(sender, instance, created, **kwargs):
    if created:
        # Create a Profile for the user
        profile = Profile.objects.create(user=instance)

        # Check if the user is in the "Drivers" group
        if Group.objects.filter(name='Drivers').exists():
            drivers_group = Group.objects.get(name='Drivers')
            if instance.groups.filter(name='Drivers').exists():
                profile.role = 'driver'
                profile.save()
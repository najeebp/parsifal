from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from activities.models import Activity

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)

    def get_screen_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user.username

    def get_followers(self):
        activities = Activity.objects.filter(from_user__pk=self.pk, activity_type=Activity.FOLLOW)
        followers = []
        for activity in activities:
            followers.append(activity.to_user)
        return followers

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
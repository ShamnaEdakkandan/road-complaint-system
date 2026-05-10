from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Profile(models.Model):
    ROLE_CHOICES =[
        ('citizen','Citizen'),
        ('engineer','Engineer'),

    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='citizen')

    def __str__(self):
        return self.user.username
    

class Complaint(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('progress','In Progress'),
        ('completed','Completed'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image=models.ImageField(upload_to='complaints/',null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    assigned_to=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
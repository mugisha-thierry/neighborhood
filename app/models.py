from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    my_location  = models.CharField(max_length=128)
    my_neighborhood_name = models.CharField(max_length=128)
    profile_pic = models.ImageField(upload_to='profile/', default='a.png')

    @classmethod
    def search_by_profile(cls, username):
        certain_user = cls.objects.filter(user__username__icontains = username)
        return certain_user

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
         if created:
            Profile.objects.create(user=instance)
            instance.profile.save()   

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile    

class Neighbourhood(models.Model):
    neighbourhood_name = models.CharField(max_length=250)
    neighbourhood_location = models.CharField(max_length=250)
    occupants_count = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='neighbourhood')

    class Meta:
        ordering = ["pk"]  

    def save_neighbourhood(self):
        self.save()

    # def get_absolute_url(self):
    #     return f"/project/{self.id}"


    def delete_neighbourhood(self):
        self.delete()

    @classmethod
    def search_by_neighbourhood(cls,search_term):
        certain_user = cls.objects.filter(title__icontains = search_term)
        return certain_user
  

    def __str__(self):
        return self.neighbourhood_name

class Neighbourhood_infrastructure(models.Model):
    CHOICES = (
        ('health','health'),
        ('fire', 'fire'),
        ('police', 'police'),
        ('emergence', 'emergence'),
        ('businesses','businesses'),
        ('market','market'),
    )
    infrastructure_name = models.CharField(max_length=250)
    infrastructure_location = models.CharField(max_length=250)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    department_name = models.CharField(max_length=300, choices=CHOICES)
    infrastructure_description = models.TextField(max_length=500, blank=True, default='No description')
    user = models.ForeignKey(Profile,null=True, on_delete=models.SET_NULL, related_name='neighbourhood_user')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='Neighbourhood_infrastructures')

    class Meta:
        ordering = ["pk"]  

    def save_Neighbourhood_infrastructure(self):
        self.save()

    # def get_absolute_url(self):
    #     return f"/project/{self.id}"

    def search_by_department(cls, username):
        certain_user = cls.objects.filter(user__username__icontains = username)
        return certain_user


    def delete_Neighbourhood_infrastructure(self):
        self.delete()

    @classmethod
    def search_by_Neighbourhood_infrastructure(cls,search_term):
        certain_user = cls.objects.filter(title__icontains = search_term)
        return certain_user
  

    def __str__(self):
        return self.infrastructure_name        
        
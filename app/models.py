from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
# from tinymce.models import HTMLField
import datetime as dt
from django.db.models import Q

class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    my_location  = models.CharField(max_length=128)
    my_neighborhood_name = models.ForeignKey('Neighbourhood',null=True, on_delete=models.SET_NULL)
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

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/')
    # description = HTMLField()
    neighbourhood = models.ForeignKey(neighbourhood,on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.neighbourhood_name

class Neighbourhood_infrastructure(models.Model):
    CHOICES = (
        ('emergence', 'emergence'),
        ('businesses','businesses'),
    )
    department_name = models.CharField(max_length=300, choices=CHOICES)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='Neighbourhood_infrastructures')
    infrastructure_name = models.CharField(max_length=250)
    infrastructure_location = models.CharField(max_length=250)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(max_length = 254,blank=True, default='No emai provided') 
    infrastructure_description = models.TextField(max_length=500, blank=True, default='No description')
    user = models.ForeignKey(Profile,null=True, on_delete=models.SET_NULL, related_name='neighbourhood_user')
    

    class Meta:
        ordering = ["pk"]  

    def save_Neighbourhood_infrastructure(self):
        self.save()


    def delete_Neighbourhood_infrastructure(self):
        self.delete()

    @classmethod
    def search_by_Neighbourhood_infrastructure(cls,search_term):
        certain_user = cls.objects.filter(infrastructure_name__icontains = search_term)
        return certain_user  
  

    def __str__(self):
        return self.infrastructure_name        
        

    @classmethod
    def delete_neighbourhood(cls,neighbourhood):
        cls.objects.filter(neighbourhood=neighbourhood).delete()


    
         

class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='post/')
    # post = HTMLField()
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    neighbourhood= models.ForeignKey(neighbourhood,on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return self.title    

    @classmethod
    def search_post(cls,search_term):
        posts = cls.objects.filter(Q(username__username=search_term) | Q(neighbourhood__neighbourhood=search_term) | Q(title__icontains=search_term))
        return posts              

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posting', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rate')
    commenting = models.TextField(max_length=500, blank=True, default='No comments')
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save_comment(self):
        self.save()

    class Meta:
        ordering = ["-pk"]                 
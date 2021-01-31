from django.contrib import admin
from .models import Profile, Neighbourhood,Neighbourhood_infrastructure,Post

# Register your models here.

admin.site.register(Neighbourhood)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Neighbourhood_infrastructure)
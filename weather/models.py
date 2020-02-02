from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
       
    class Meta:
        verbose_name_plural = 'cities'

    def save(self, *args, **kwargs):
        self.name = (self.name.capitalize())
        mycities = City.objects.filter(name = self.name)
        if len(mycities):
            """This city is in database"""
            return 
        else:
            super().save(*args, **kwargs)
    
    def delete(self, myuser, *args, **kwargs):
        citylist = CityList.objects.filter(user=myuser)
        if len(citylist) == 0:
            raise 'Error'
        else:
            citylist[0].cities.remove(self)

        if self.citylist_set.count():
            return
        else:
            """This city is not in any CityList"""
            super().delete(*args, **kwargs)        

class CityList(models.Model):
    user = models.ForeignKey("auth.User", on_delete = models.CASCADE)
    cities = models.ManyToManyField(City)
    subscription = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.user.username + " City List"
    
    def send_forecast_report(self):
        print(self.cities.all())



    


        

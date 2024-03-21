from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone

class Ride(models.Model):
    STATUS_CHOICES=[
        ('requested','Requested'),
        ('accepted','Accepted'),
        ('completed','Completed'),
        ('canceled','Canceled')
    ]
    
    rider=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='ride_requested',on_delete=models.CASCADE)
    driver=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='ride_accepted',null=True,blank=True,on_delete=models.CASCADE)
    pickup_location=models.PointField()
    dropoff_location=models.PointField()
    current_location=models.PointField(null=True, blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='requested')    
    created_at=models.DateTimeField(default=timezone.now, editable=False)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Ride {self.id} - {self.rider.username}'   

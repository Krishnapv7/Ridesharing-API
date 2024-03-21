from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response 
from .models import Ride
from .serializers import RideSerializer 

class RideViewSet(viewsets.ModelViewSet):
    queryset=Ride.objects.all()
    serializer_class=RideSerializer
    
    @action(detail=True,methods=['post'])
    def start_ride(self,request,pk=None):
        ride=self.get_object()
        ride.status='accepted'
        ride.save()
        serializer=self.get_serializer(ride)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def  complete_ride(self,request,pk=None):
        ride=self.get_object()
        ride.status='completed'
        ride.save()
        serializer=self.get_serializer(ride)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def cancel_ride(self,request,pk=None):
        ride=self.get_object()
        ride.status='canceled'
        ride.save()
        serializer=self.get_serializer(ride)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def update_location(self,request,pk=None):
        ride=self.get_object()
        current_location=self.request.data.get('current_location')
        ride.current_location=current_location
        ride.save()
        serializer=self.get_serializer(ride)
        return Response(serializer.data)
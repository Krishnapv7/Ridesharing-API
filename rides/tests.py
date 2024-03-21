from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Ride


class RideMatchingAlgorithmTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(username='rider',password='testpassword1')
        self.driver = User.objects.create_user(username='driver',password='testpasssword2')
        self.client = APIClient()
        self.client.force_authenticate(user=self.rider)
        
    def test_ride_matching_algorithm(self):
        
        ride_data = {
            'rider':self.rider.id,
            'pickup_location':'POINT(0 0)',
            'dropoff_location':'POINT(0 0)',
            'status':'requested'
        }
        
        ride_request=Ride.objects.create(**ride_data)
        
        self.client.force_authenticate(user=self.driver)
        url=reverse('ride-accept-ride',args=[ride_request.id])
        response=self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['status'],'accepted')
        
        ride_request.refresh_from_db()
        self.assertEqual(ride_request.driver,self.driver)
        
        
class RideStatusUpdateTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(username='rider',password='testpassword1')
        self.driver = User.objects.create_user(username='driver',password='testpasssword2')
        self.client = APIClient()
        self.client.force_authenticate(user=self.rider)
        
    def test_ride_status_updates(self):
        
        ride_data={
            'rider':self.rider.id,
            'pickup_location':'POINT(0 0)',
            'dropoff_location':'POINT(0 0)',
            'status':'requested'
        }
    
        ride_request=Ride.objects.create(**ride_data)
        
        self.client.force_authenticate(user=self.driver)
        url = reverse('ride-start-ride',args=[ride_request.id])
        response=self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['status'],'started')
        
        
        self.client.force_authenticate(user=self.rider)
        url=reverse('ride-complete-ride',args=[ride_request.id])
        response=self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['status'],'completed')
        
        
class DriverAPITest(TestCase):
    def setUp(self):
        self.driver=User.objects.create_user(username='driver',password='testpassword2')
        self.client=APIClient()
        self.client.force_authenticate(user=self.driver)
        
    def test_list_accepted_ride(self):
        ride_data={
            'rider':User.objects.create_user(username='rider',password='testpassword1').id,
            'pickup_location':'POINT(0 0)',
            'dropoff_location':'POINT(0 0)',
            'status':'accepted',
            'driver':self.driver.id
        }
        Ride.objects.create(**ride_data)
        
        url=reverse('driver_list_accepted_rides')
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        

class RideTrackingSimulationTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(username='rider', password='testpassword1')
        self.driver = User.objects.create_user(username='driver', password='testpassword2')
        self.client = APIClient()
        self.client.force_authenticate(user=self.rider)

    def test_update_location(self):
        
        ride_data = {
            'rider': self.rider.id,
            'pickup_location': 'POINT(0 0)',
            'dropoff_location': 'POINT(1 1)',
            'status': 'started',
            'driver': self.driver.id,
            'current_location': 'POINT(0.5 0.5)'
        }
        ride = Ride.objects.create(**ride_data)

        
        url = reverse('ride-update-location', args=[ride.id])
        updated_location = 'POINT(0.6 0.6)'
        response = self.client.post(url, {'current_location': updated_location}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_location'], updated_location)
        
        

                  
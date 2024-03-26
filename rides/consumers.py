import json
from channels.generic.websocket import WebsocketConsumer

class RideConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.group_name = f"ride_{ride_id}"
        self.channel_layer.group_add(self.group_name,self.channel_name)
        
    def disconnect(self,close_code):
        self.channel_layer.group_discard(self.group_name,self.channel_name)
        
    def receive(self,text_data):
        pass
    
    def update_location(self,event):
        latitude = event['latitude']
        longitude = event['longitude']
        
        self.send(text_data=json.dumps({
            'latitude' : latitude,
            'longitude' : longitude
        }))        
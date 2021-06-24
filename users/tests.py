from django.test import Client

c = Client()

response = c.post('/user_login/',{'username':'ashwin','password':'csgo12345'})
response.status_code

# Create your tests here.

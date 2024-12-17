from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, LoginViewset, UserViewset
from .TripBuild import generate_itinerary

# Set up the router for viewsets
router = DefaultRouter()
router.register('register', RegisterViewset, basename='register')
router.register('login', LoginViewset, basename='login')
router.register('users', UserViewset, basename='users')

# Custom URL patterns for function-based views
urlpatterns = [
    path('generate-itinerary/', generate_itinerary, name='generate_itinerary'),  # Custom route
]

# Include the router URLs
urlpatterns += router.urls

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, LoginViewset, UserViewset,TripViewset, PlaceViewset, fetch_image_url_for_trip_view
from .TripBuild import generate_itinerary
from .views import fetch_image_url_view

# Set up the router for viewsets
router = DefaultRouter()
router.register('register', RegisterViewset, basename='register')
router.register('login', LoginViewset, basename='login')
router.register('users', UserViewset, basename='users')
router.register('trips', TripViewset, basename='trips')
router.register('places', PlaceViewset, basename='places')


# Custom URL patterns for function-based views
urlpatterns = [
    path('api/', include(router.urls)),
    path('generate-itinerary/', generate_itinerary, name='generate_itinerary'),  # Custom route
    path('api/fetch-image-url/', fetch_image_url_view, name='fetch_image_url'),
    path('api/fetch-image-url-for-trip/', fetch_image_url_for_trip_view, name='fetch_image_url_for_trip'),  # New endpoint
    
]

# Include the router URLs
urlpatterns += router.urls

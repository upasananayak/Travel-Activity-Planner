from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, permissions, status
from .serializers import * 
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework.decorators import api_view
import google.generativeai as genai
from .utils import fetch_image_url,fetch_image_url_for_trip
import requests


User = get_user_model()

class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request): 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user: 
                _, token = AuthToken.objects.create(user)
                return Response(
                    {
                        "user": self.serializer_class(user).data,
                        "token": token
                    }
                )
            else: 
                return Response({"error":"Invalid credentials"}, status=401)    
        else: 
            return Response(serializer.errors, status=400)

class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=400)

class UserViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # def generate_itinerary(self, request):
    #     """
    #     Takes inputs: city, days, visit date, number of people, and interests.
    #     Queries the Gemini API to generate a day-wise itinerary and returns it as JSON.
    #     """
    #     print("CALL")
    #     city = request.data.get('city')
    #     days = request.data.get('days')
    #     visit_date = request.data.get('visit_date')
    #     num_people = request.data.get('num_people')
    #     interests = request.data.get('interests')

    #     # Validate inputs
    #     if not all([city, days, visit_date, num_people, interests]):
    #         return Response({"error": "All fields (city, days, visit_date, num_people, interests) are required."},
    #                         status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Configure the GenAI client
    #         genai.configure(api_key=GEMINI_API_KEY)
    #         model = genai.GenerativeModel("gemini-1.5-flash")

    #         # Create the prompt for the itinerary
    #         prompt = (
    #             f"I am visiting {city} for {days} days starting from {visit_date} with {num_people} people. "
    #             f"Our interests include {', '.join(interests)}. "
    #             f"Please provide a detailed day-wise itinerary including must-visit places, activities, and timing suggestions."
    #         )

    #         # Generate content using the Gemini API
    #         response = model.generate_content(prompt)
    #         print(response)
    #         # Extract the response text
    #         try:
    #             response_text = response.text
    #             itinerary = response_text.strip()
    #         except AttributeError:
    #             return Response({"error": "Invalid response format from Gemini API"},
    #                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #         return Response({"itinerary": itinerary}, status=status.HTTP_200_OK)

    #     except Exception as e:
    #         return Response({"error": "An unexpected error occurred: " + str(e)},
    #                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TripViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TripSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("User not authenticated")
        return Trip.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        trip = serializer.save()
        if trip.image_url=='https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg':
            try:
                image_url = fetch_image_url_for_trip(trip.place)
                trip.image_url = image_url
                trip.save()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching image URL for trip {trip.id}: {e}")

    def perform_update(self, serializer):
        trip = serializer.save()
        if trip.image_url=='https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg':
            try:
                image_url = fetch_image_url_for_trip(trip.place)
                trip.image_url = image_url
                trip.save()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching image URL for trip {trip.id}: {e}")

class PlaceViewset(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Place.objects.filter(trip__user=self.request.user)

    def perform_create(self, serializer):
        trip_id = self.request.data.get('trip')
        trip = Trip.objects.filter(id=trip_id, user=self.request.user).first()

        if not trip:
            raise PermissionDenied("You don't have permission to add a place to this trip.")

        # Automatically calculate the next order value
        next_order = Place.objects.filter(trip=trip).count() + 1

        place = serializer.save(trip=trip, order=next_order, visited=False)

        # Check if the image URL is the placeholder and fetch the actual image URL
        if place.image_url == 'https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg':
            try:
                image_url = fetch_image_url(place.name, trip.id)
                place.image_url = image_url
                place.save()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching image URL for place {place.id}: {e}")

    def perform_update(self, serializer):
        place = serializer.save()

        # Check if the image URL is the placeholder and fetch the actual image URL
        if place.image_url == 'https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg':
            try:
                image_url = fetch_image_url(place.name, place.trip.id)
                place.image_url = image_url
                place.save()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching image URL for place {place.id}: {e}")



@api_view(['GET'])
def fetch_image_url_view(request):
    place_name = request.GET.get('place_name')
    trip_id = request.GET.get('trip_id')
    if not place_name or not trip_id:
        return JsonResponse({"error": "place_name and trip_id parameters are required"}, status=400)
    print(f"place_name: {place_name}, trip_id: {trip_id}")
    place_name = request.query_params.get('place_name')
    trip_id = request.query_params.get('trip_id')
    if not place_name or not trip_id:
        return Response({'error': 'place_name and trip_id parameters are required'}, status=400)
    try:
        image_url = fetch_image_url(place_name, trip_id)
        return Response({'image_url': image_url})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=429)
        return Response({'error': str(e)}, status=500)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def fetch_image_url_for_trip_view(request):
    place = request.query_params.get('place')
    if not place:
        return Response({'error': 'place parameter is required'}, status=400)
    try:
        image_url = fetch_image_url_for_trip(place)
        return Response({'image_url': image_url})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=429)
        return Response({'error': str(e)}, status=500)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)
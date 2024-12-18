from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .serializers import * 
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework.decorators import api_view
import google.generativeai as genai

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
    permission_classes = [permissions.AllowAny]
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

# views.py

# views.py

class PlaceViewset(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        trip_id = self.request.data.get('trip_id')
        trip = Trip.objects.get(id=trip_id, user=self.request.user)
        serializer.save(trip=trip)
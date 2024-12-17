from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_date
from .models import Trip, Place, CustomUser
import google.generativeai as genai
from django.conf import settings

GEMINI_API_KEY = settings.GEMINI_API_KEY

@api_view(['POST'])
def generate_itinerary(request):
    """
    Takes inputs: city, days, visit date, number of people, and interests.
    Queries the Gemini API to generate a day-wise itinerary,
    populates the Trip and Place tables, and returns the itinerary as JSON.
    """
    city = request.data.get('city')
    days = request.data.get('days')
    visit_date = request.data.get('visit_date')
    num_people = request.data.get('num_people')
    interests = request.data.get('interests')

    userMail = request.user
    if not userMail or not userMail.is_authenticated:
        return Response(
            {"error": "Unauthorized request. Access Denied."},
            status=401
        )
    
    try:
        user = CustomUser.objects.get(email=userMail)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Unauthorized request. Access Denied."},
            status=401
        )
    
    if not all([city, days, visit_date, num_people, interests]):
        return Response(
            {"error": "All fields (city, days, visit_date, num_people, interests) are required."},
            status=400
        )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"I am visiting {city} for {days} days starting from {visit_date} with {num_people} people. "
            f"Our interests include {', '.join(interests)}. "
            f"Please provide a detailed day-wise itinerary including must-visit places, activities, hyperlinks for each site, and timing suggestions."
        )
        response = model.generate_content(prompt)
        itinerary = response.text.strip() if hasattr(response, 'text') else None
        
        if not itinerary:
            return Response(
                {"error": "Invalid response format from Gemini API"},
                status=500
            )        

        listPrompt = (
            f"Convert the below itinerary into just a list of places separated by commas. "
            f"{response.text}"
        )
        listedResponse = model.generate_content(listPrompt)
        listedResponse = listedResponse.text.strip() if hasattr(listedResponse, 'text') else None

        if not listedResponse:
            return Response(
                {"error": "Unable to extract a list of places from the response."},
                status=500
            )

        trip = Trip.objects.create(
            user=user,
            starting_date=parse_date(visit_date),
            place=city,
            number_of_days=int(days),
        )


        places_list = listedResponse.split(",")
        for idx, place_name in enumerate(places_list, start=1):
            Place.objects.create(
                trip=trip,
                name=place_name.strip(),
                order=idx 
            )

        return Response({
            "itinerary": itinerary,
            "places": [place_name.strip() for place_name in places_list],
            "message": "Trip and places successfully saved."
        }, status=200)

    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=500
        )

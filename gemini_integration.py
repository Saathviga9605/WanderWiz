import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def generate_itinerary(destination, experience, transportation, travelStyle, dietaryRestrictions, month, budget, interests, duration):
    prompt = (f"Create a personalized travel itinerary for the following details: "
              f"Destination: {destination}. "
              f"Experience: {', '.join(experience)}. "
              f"Transportation: {', '.join(transportation)}. "
              f"Travel Style: {travelStyle}. "
              f"Dietary Restrictions: {dietaryRestrictions}. "
              f"Month: {month}. "
              f"Budget: ${budget}. "
              f"Interests: {', '.join(interests)}. "
              f"Duration: {duration} days.")

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([prompt])
    return response.text.strip()

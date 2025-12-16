from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
import json
import requests
from datetime import datetime, timedelta

# Tool 1: Flight Search
def search_flights(query: str) -> str:
    """Search for flights based on source and destination"""
    try:
        params = json.loads(query)
        source = params.get('source', '').lower()
        destination = params.get('destination', '').lower()
        
        with open('data/flights.json', 'r') as f:
            flights = json.load(f)
        
        filtered = [f for f in flights if 
                   source in f.get('source', '').lower() and 
                   destination in f.get('destination', '').lower()]
        
        if not filtered:
            return "No flights found"
        
        # Sort by price
        filtered.sort(key=lambda x: x.get('price', float('inf')))
        top_flights = filtered[:3]
        
        return json.dumps(top_flights, indent=2)
    except Exception as e:
        return f"Error searching flights: {str(e)}"

# Tool 2: Hotel Search
def search_hotels(query: str) -> str:
    """Search for hotels in a city"""
    try:
        params = json.loads(query)
        city = params.get('city', '').lower()
        max_price = params.get('max_price', float('inf'))
        
        with open('data/hotels.json', 'r') as f:
            hotels = json.load(f)
        
        filtered = [h for h in hotels if 
                   city in h.get('city', '').lower() and 
                   h.get('price_per_night', 0) <= max_price]
        
        if not filtered:
            return "No hotels found"
        
        # Sort by rating, then price
        filtered.sort(key=lambda x: (-x.get('rating', 0), x.get('price_per_night', 0)))
        top_hotels = filtered[:3]
        
        return json.dumps(top_hotels, indent=2)
    except Exception as e:
        return f"Error searching hotels: {str(e)}"

# Tool 3: Places Discovery
def search_places(query: str) -> str:
    """Search for tourist attractions and places"""
    try:
        params = json.loads(query)
        city = params.get('city', '').lower()
        place_type = params.get('type', '').lower()
        
        with open('data/places.json', 'r') as f:
            places = json.load(f)
        
        filtered = [p for p in places if city in p.get('city', '').lower()]
        
        if place_type:
            filtered = [p for p in filtered if place_type in p.get('type', '').lower()]
        
        if not filtered:
            return "No places found"
        
        # Sort by rating
        filtered.sort(key=lambda x: -x.get('rating', 0))
        top_places = filtered[:5]
        
        return json.dumps(top_places, indent=2)
    except Exception as e:
        return f"Error searching places: {str(e)}"

# Tool 4: Weather Lookup
def get_weather(query: str) -> str:
    """Get weather forecast for a location"""
    try:
        params = json.loads(query)
        latitude = params.get('latitude')
        longitude = params.get('longitude')
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto&start_date={start_date}&end_date={end_date}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# Tool 5: Budget Calculator
def calculate_budget(query: str) -> str:
    """Calculate total trip budget"""
    try:
        params = json.loads(query)
        flight_cost = params.get('flight_cost', 0)
        hotel_cost_per_night = params.get('hotel_cost_per_night', 0)
        num_nights = params.get('num_nights', 0)
        daily_expenses = params.get('daily_expenses', 50)  # Default $50/day
        
        total_hotel = hotel_cost_per_night * num_nights
        total_daily = daily_expenses * num_nights
        total = flight_cost + total_hotel + total_daily
        
        breakdown = {
            "flight": flight_cost,
            "hotel": total_hotel,
            "daily_expenses": total_daily,
            "total": total
        }
        
        return json.dumps(breakdown, indent=2)
    except Exception as e:
        return f"Error calculating budget: {str(e)}"

# Create LangChain Tools
tools = [
    Tool(
        name="FlightSearch",
        func=search_flights,
        description="Searches for flights. Input should be JSON with 'source' and 'destination' keys. Returns top 3 cheapest flights."
    ),
    Tool(
        name="HotelSearch",
        func=search_hotels,
        description="Searches for hotels. Input should be JSON with 'city' and optionally 'max_price' keys. Returns top rated hotels."
    ),
    Tool(
        name="PlaceSearch",
        func=search_places,
        description="Searches for tourist places and attractions. Input should be JSON with 'city' and optionally 'type' keys. Returns top rated places."
    ),
    Tool(
        name="WeatherForecast",
        func=get_weather,
        description="Gets weather forecast. Input should be JSON with 'latitude', 'longitude', 'start_date', and 'end_date' (YYYY-MM-DD format)."
    ),
    Tool(
        name="BudgetCalculator",
        func=calculate_budget,
        description="Calculates trip budget. Input should be JSON with 'flight_cost', 'hotel_cost_per_night', 'num_nights', and 'daily_expenses'."
    )
]

# Agent Prompt Template
template = """You are an expert travel planning assistant. Use the available tools to create comprehensive travel itineraries.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (must be valid JSON)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT: Always provide detailed, structured itineraries with:
1. Flight recommendations with reasoning
2. Hotel recommendations with justification
3. Day-by-day itinerary with specific places
4. Weather forecast for each day
5. Complete budget breakdown

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

def create_travel_agent():
    """Create and return the LangChain agent"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    return agent_executor

def generate_itinerary_with_agent(destination, experience, transportation, 
                                   travelStyle, dietaryRestrictions, month, 
                                   budget, interests, duration, source_city=None):
    """Generate itinerary using LangChain agent"""
    
    agent_executor = create_travel_agent()
    
    # Construct the query for the agent
    query = f"""Create a detailed {duration}-day travel itinerary for {destination} with the following preferences:
    
- Travel from: {source_city if source_city else 'any major city'}
- Travel experiences desired: {', '.join(experience)}
- Transportation preferences: {', '.join(transportation)}
- Travel style: {travelStyle}
- Dietary restrictions: {dietaryRestrictions}
- Month of travel: {month}
- Total budget: ${budget}
- Interests: {', '.join(interests)}
- Duration: {duration} days

Please use the available tools to:
1. Find the best flight options
2. Recommend suitable hotels
3. Discover top-rated attractions and places
4. Check weather forecast
5. Calculate detailed budget breakdown

Provide a comprehensive day-by-day itinerary with specific recommendations and reasoning."""

    try:
        result = agent_executor.invoke({"input": query})
        return result['output']
    except Exception as e:
        return f"Error generating itinerary: {str(e)}"

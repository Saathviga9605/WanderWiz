
# WanderWiz - AI Travel Planning Assistant

Welcome to WanderWiz, an intelligent travel planning application powered by LangChain and Agentic AI. This application generates comprehensive, personalized travel itineraries by autonomously searching flights, hotels, attractions, checking weather forecasts, and calculating budgets—all tailored to your preferences.

## Features

* **Agentic AI Planning** : Uses LangChain ReAct agents to autonomously plan trips with multi-step reasoning
* **Real-time Flight Search** : Finds the best flight options from curated datasets
* **Hotel Recommendations** : Suggests accommodations based on rating, location, and budget
* **Places Discovery** : Recommends top-rated attractions and points of interest
* **Live Weather Integration** : Fetches real-time weather forecasts using Open-Meteo API (no API key required)
* **Budget Breakdown** : Provides detailed cost estimates including flights, hotels, and daily expenses
* **Day-wise Itineraries** : Generates structured day-by-day travel plans
* **Dynamic Frontend** : Built with HTML, CSS, and JavaScript for a responsive user experience
* **Multilingual Support** : Translates the webpage into 50 languages using Google Translate API
* **Interactive UI** : Dynamically updates options based on user selections

## Application Architecture

### Frontend
* **HTML** : Structures the user interface with interactive form elements
* **CSS** : Modern styling with animations and responsive design
* **JavaScript** : Manages interactivity, dynamic dropdowns, and AJAX requests

### Backend
* **Flask** : Lightweight Python web framework for API handling
* **LangChain** : Agentic AI framework with ReAct agents for autonomous planning
* **OpenAI API** : Powers the language model for intelligent decision-making
* **JSON Datasets** : Local storage for flights, hotels, and places data
* **Open-Meteo API** : Free weather forecasting service (no authentication required)

### Tools & Capabilities
The AI agent has access to five specialized tools:
1. **FlightSearch** - Finds and ranks flights by price and convenience
2. **HotelSearch** - Recommends hotels by rating and price
3. **PlaceSearch** - Discovers attractions filtered by type and rating
4. **WeatherForecast** - Retrieves multi-day weather predictions
5. **BudgetCalculator** - Computes total trip costs with itemized breakdown

## Project Structure

```
wanderwiz/
├── app.py                      # Flask application entry point
├── langchain_agent.py          # LangChain agent and tool definitions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── data/
│   ├── flights.json           # Flight dataset
│   ├── hotels.json            # Hotel dataset
│   └── places.json            # Tourist attractions dataset
├── templates/
│   ├── index.html             # Main form page
│   └── result.html            # Itinerary display page
└── static/
    ├── css/
    │   └── styles.css         # Styling and animations
    ├── js/
    │   └── script.js          # Frontend interactivity
    └── images/
        └── travel*.png        # Decorative images
```

## Skills Demonstrated

* **Python Programming** - Clean, modular code with proper error handling
* **LLM Integration** - OpenAI API integration with LangChain
* **Agentic AI (LangChain)** - ReAct agents with autonomous decision-making
* **Prompt Engineering** - Structured prompts for reliable agent behavior
* **API Integration** - External weather API and internal tool coordination
* **Web Development** - Flask backend with dynamic frontend
* **Data Processing** - JSON file handling and filtering algorithms

## Setup and Installation

### Prerequisites
* Python 3.8 or higher
* OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
* Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/wanderwiz.git
cd wanderwiz
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download Dataset Files

1. Download the JSON datasets
2. Create a `data/` folder in the project root
3. Place `flights.json`, `hotels.json`, and `places.json` in the `data/` folder

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**Note**: Never commit your `.env` file to version control. Add it to `.gitignore`.

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

1. **Fill out the travel form** with your preferences:
   - Source city (where you're traveling from)
   - Destination city
   - Trip duration (number of days)
   - Budget in USD
   - Month of travel
   - Travel style (Adventure, Luxury, Family, etc.)
   - Experiences (select up to 3)
   - Interests and dietary restrictions

2. **Submit the form** - The AI agent will:
   - Search for optimal flights
   - Find suitable hotels
   - Discover top attractions
   - Check weather forecasts
   - Calculate total costs
   - Generate a day-by-day itinerary

3. **Review your itinerary** - Get a comprehensive plan including:
   - Selected flight with price and timing
   - Recommended hotel with rating and nightly rate
   - Day-wise activity suggestions
   - Weather forecast for each day
   - Complete budget breakdown

## Example Output

```
Your 3-Day Trip to Goa (Feb 12–14, 2025)

Flight Selected:
- IndiGo Flight #AI203 (₹4,800)
- Departs: Delhi at 14:00 | Arrives: Goa at 16:30

Hotel Recommended:
- Sea View Resort (4.5⭐, ₹3,200/night)
- Beachfront location with pool and spa

Weather Forecast:
- Day 1 (Feb 12): Sunny, 31°C
- Day 2 (Feb 13): Partly Cloudy, 29°C
- Day 3 (Feb 14): Light Breeze, 30°C

Day-by-Day Itinerary:

Day 1: Arrival & Beach Exploration
- Morning: Check-in at hotel
- Afternoon: Baga Beach (4.6⭐)
- Evening: Candolim Market

Day 2: Heritage & Culture
- Morning: Basilica of Bom Jesus (4.8⭐)
- Afternoon: Old Goa Heritage Walk
- Evening: Local cuisine tour

Day 3: Adventure & Departure
- Morning: Water Sports at Calangute Beach
- Afternoon: Souvenir shopping
- Evening: Flight back to Delhi

Budget Breakdown:
- Flight (Round trip): ₹4,800
- Hotel (2 nights): ₹6,400
- Daily Expenses (Food, Transport): ₹2,500
- Activities & Misc: ₹1,000
-------------------------------------
Total Estimated Cost: ₹14,700
```

## Optional: Streamlit Interface

For a simpler UI alternative, run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.


Thank you for checking out WanderWiz! Happy travels! ✈️🌍

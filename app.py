from flask import Flask, request, jsonify, render_template
from langchain_agent import generate_itinerary_with_agent
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/generate-itinerary', methods=['POST'])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    destination = data.get('destination')
    experience = data.get('experience', [])
    transportation = data.get('transportation', [])
    travelStyle = data.get('travelStyle', 'Leisure')
    dietaryRestrictions = data.get('dietaryRestrictions', 'No')
    month = data.get('month')
    budget = data.get('budget')
    interests = data.get('interests', [])
    duration = data.get('duration')
    source_city = data.get('sourceCity', None)

    try:
        itinerary = generate_itinerary_with_agent(
            destination, experience, transportation, travelStyle, 
            dietaryRestrictions, month, budget, interests, duration, source_city
        )
        return jsonify({'itinerary': itinerary})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error generating itinerary. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

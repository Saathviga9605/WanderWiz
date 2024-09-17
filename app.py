from flask import Flask, request, jsonify, render_template
from gemini_integration import generate_itinerary

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
    experience = data.get('experience')
    transportation = data.get('transportation')
    travelStyle = data.get('travelStyle')
    dietaryRestrictions = data.get('dietaryRestrictions')
    month = data.get('month')
    budget = data.get('budget')
    interests = data.get('interests')
    duration = data.get('duration')

    try:
        itinerary = generate_itinerary(destination, experience, transportation, travelStyle, dietaryRestrictions, month, budget, interests, duration)
        return jsonify({'itinerary': itinerary})
    except Exception as e:
        return jsonify({'error': 'Error generating itinerary. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

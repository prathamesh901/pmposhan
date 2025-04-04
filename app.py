from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import json  # Ensure safe JSON handling

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS

# Configure Google Gemini AI API key
API_KEY = "AIzaSyBxcJsKgmy5RXZRmzpAPlQzkWfytkINn2c"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        image_file = request.files['image']
        image = Image.open(image_file)

        # Generate food names and calorie data
        response_food = model.generate_content([
            "Identify the food items in this image and provide their approximate calorie values per 100g. "
            "Respond only in JSON format as follows: "
            '[{"name": "apple", "calories_per_100g": 52}, {"name": "banana", "calories_per_100g": 89}]',
            image
        ])

        # Extract text response & ensure it's valid JSON
        food_response_text = response_food.text.strip()
        
        # Attempt to parse as JSON
        try:
            food_data = json.loads(food_response_text)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid response from AI"}), 500

        # Generate food quality assessment
        response_quality = model.generate_content([
            "Assess the food quality in this image and return only 'Good' or 'Bad'.",
            image
        ])
        quality = "Good" if "good" in response_quality.text.lower() else "Bad"

        # Return structured JSON output
        result = {"food_items": food_data, "quality": quality}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors gracefully

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

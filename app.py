from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import json
import re  # Import regex for cleaning AI response

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
            "Respond strictly in JSON format: "
            '[{"name": "apple", "calories_per_100g": 52}, {"name": "banana", "calories_per_100g": 89}]',
            image
        ])

        # Extract response text
        food_response_text = response_food.text.strip()

        # Use regex to extract only JSON part
        json_match = re.search(r'\[.*\]', food_response_text, re.DOTALL)

        if json_match:
            json_data = json_match.group(0)  # Extract matched JSON
            try:
                food_data = json.loads(json_data)  # Parse JSON safely
            except json.JSONDecodeError:
                return jsonify({"error": "AI returned malformed JSON"}), 500
        else:
            return jsonify({"error": "No valid JSON found in AI response"}), 500

        # Format: ["name value"]
        formatted_items = [f"{item['name']} {item['calories_per_100g']}" for item in food_data]

        # Generate food quality assessment
        response_quality = model.generate_content([
            "Assess the food quality in this image. Respond with only 'Good' or 'Bad'.",
            image
        ])
        quality = "Good" if "good" in response_quality.text.lower() else "Bad"

        # Return structured output
        result = {"food_items": formatted_items, "quality": quality}
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors gracefully

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

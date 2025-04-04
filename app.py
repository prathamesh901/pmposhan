from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS

# Configure Google Gemini API key
API_KEY = "your_api_key_here"
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify([]), 400  # Return empty list if no image uploaded

    try:
        image_file = request.files['image']
        image = Image.open(image_file)

        # Generate food names and calorie values
        prompt = """
        Identify the food items in this image and provide their approximate calorie values per 100g.
        Respond in the following JSON format:
        {
            "food_items": [
                {"name": "apple", "calories_per_100g": 52},
                {"name": "banana", "calories_per_100g": 89}
            ]
        }
        """
        response_food = model.generate_content([prompt, image])
        
        # Parse response text as JSON
        food_data = eval(response_food.text)  # Make sure the response is properly formatted

        # Assess food quality (Good or Bad)
        response_quality = model.generate_content([
            "Assess the food quality in this image and return only 'Good' or 'Bad'.", image
        ])
        quality = "Good" if "good" in response_quality.text.lower() else "Bad"

        # Return structured JSON output
        result = {"food_items": food_data["food_items"], "quality": quality}

        return jsonify(result)  # Return JSON response

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error if any issue occurs

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

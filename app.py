from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS

# Configure Google Gemini AI API key
API_KEY = "AIzaSyBxcJsKgmy5RXZRmzpAPlQzkWfytkINn2c"
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify([]), 400  # Return empty list if no image uploaded

    try:
        image_file = request.files['image']
        image = Image.open(image_file)

        # Generate food names based on the image
        response = model.generate_content(["List only the food names, without any extra text.", image])
        food_items = [item.strip("* ") for item in response.text.strip().split("\n") if item.strip()]

        return jsonify(food_items)  # Return clean JSON output with only food names

    except Exception as e:
        return jsonify([]), 500  # Return empty list on error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Configure Google Gemini AI API key
API_KEY = "AIzaSyBxcJsKgmy5RXZRmzpAPlQzkWfytkINn2c"
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        # Get the image file from the request
        image_file = request.files['image']
        image = Image.open(image_file)

        # Generate food names based on the image
        response = model.generate_content(["List the name of foods based on this picture.", image])

        # Ensure response is properly formatted as JSON
        food_items = response.text.strip().split("\n")  # Convert response text to a list

        return jsonify({'food_items': food_items})  # Return JSON response

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error in JSON format

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

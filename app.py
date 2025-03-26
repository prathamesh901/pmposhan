from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import io

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
    print("Received files:", request.files)  # Debugging line

    if not request.files:
        return jsonify({'error': 'No files received'}), 400

    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded', 'message': 'Make sure you are sending form-data with key as "image".'}), 400

    try:
        image_file = request.files['image']
        image = Image.open(image_file)

        # Generate food names based on the image
        response = model.generate_content(["List the name of foods based on this picture.", image])
        food_items = response.text.strip().split("\n")

        return jsonify({'food_items': food_items}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)





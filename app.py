from flask import Flask, request, jsonify
import pickle
import numpy as np
from PIL import Image
import io

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained AI model
MODEL_PATH = "model.pkl"  # Replace with your model's .pkl file path
with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

# Define a function to preprocess the image
def preprocess_image(image_bytes):
    # Open the image
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    # Resize the image to the input size expected by your model
    image = image.resize((224, 224))  # Example size, adjust as needed
    # Convert the image to a NumPy array
    image_array = np.array(image)
    # Normalize the image (e.g., scale pixel values to 0-1 if required)
    image_array = image_array / 255.0
    # Reshape for model input (add batch dimension if necessary)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# Define the endpoint for image upload
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file is uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']

    # Ensure the file is a .jpg image
    if not file.filename.endswith('.jpg'):
        return jsonify({'error': 'Only .jpg files are allowed'}), 400

    try:
        # Read the image file and preprocess it
        image_bytes = file.read()
        processed_image = preprocess_image(image_bytes)

        # Make a prediction
        prediction = model.predict(processed_image)

        # Convert the prediction to "True" or "False"
        result = bool(np.round(prediction[0]))  # Adjust based on your model's output
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
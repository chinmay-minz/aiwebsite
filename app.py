from fenlask import Flask, request, jsonify, render_template
import tensorflow as tf
import cv2
import numpy as np
import io

app = Flask(__name__)

# Load the pre-trained AI model from TensorFlow
MODEL_PATH = "counterfeitmodel.h5"  # Path to your TensorFlow model (e.g., .h5 format)
model = tf.keras.models.load_model(MODEL_PATH)

# Preprocessing function using OpenCV and TensorFlow
def preprocess_image(image_bytes):
    # Convert image bytes to a NumPy array (using OpenCV)
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Resize the image to match the model input size (224x224 for many models)
    image = cv2.resize(image, (224, 224))

    # Normalize the pixel values (0-255 to 0.0-1.0)
    image = image / 255.0

    # Convert to the shape expected by TensorFlow (batch_size, height, width, channels)
    image = np.expand_dims(image, axis=0)
    
    return image

# Route to serve the main page
@app.route('/')
def index():
    return render_template('aidhanraksak.html')  # Serves 'templates/index.html'

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
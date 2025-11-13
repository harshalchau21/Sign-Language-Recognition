from flask import Flask, render_template, request, jsonify
from keras.models import load_model
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
model = load_model('my_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_data = data['image'].split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = np.array(image)
    image = cv2.resize(image, (400, 400))
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return jsonify({'prediction': chr(predicted_class + 65)})

if __name__ == '__main__':
    app.run(debug=True)

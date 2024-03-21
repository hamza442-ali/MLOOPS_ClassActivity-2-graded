from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import tensorflow as tf

app = Flask(_name_)

# Load the trained model
loaded_model = tf.keras.models.load_model('model.h5')

# Define class names
class_names = ['Black Soil', 'Cinder Soil', 'Laterite Soil', 'Peat Soil', 'Yellow Soil']

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image file from the request
    file = request.files['file']
    
    # Load the image
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(img_array)
    
    # Make predictions
    predictions = loaded_model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)
    predicted_class = class_names[predicted_class_index[0]]
    
    return jsonify({'prediction': predicted_class})

if _name_ == '_main_':
    app.run(debug=True)
import os
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model():
    # Load pre-trained EfficientNet model
    model = tf.keras.applications.EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Add custom layers for deepfake detection
    x = model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    predictions = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    
    model = tf.keras.Model(inputs=model.input, outputs=predictions)
    
    # Load pre-trained weights (you would need to download these)
    # model.load_weights('path_to_weights.h5')
    
    return model

def preprocess_image(image_path):
    # Read image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize image
    img = cv2.resize(img, (224, 224))
    
    # Normalize pixel values
    img = img.astype('float32') / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img

def process_video(video_path):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize frame
        frame = cv2.resize(frame, (224, 224))
        
        # Normalize pixel values
        frame = frame.astype('float32') / 255.0
        
        frames.append(frame)
    
    cap.release()
    
    # Convert frames to numpy array
    frames = np.array(frames)
    
    return frames

def detect_deepfake_image(image_path):
    # Preprocess image
    img = preprocess_image(image_path)
    
    # Make prediction
    prediction = model.predict(img)[0][0]
    
    return {
        'is_deepfake': bool(prediction > 0.5),
        'confidence': float(prediction)
    }

def detect_deepfake_video(video_path):
    # Process video
    frames = process_video(video_path)
    
    # Make predictions for each frame
    predictions = model.predict(frames)
    
    # Calculate average prediction
    avg_prediction = np.mean(predictions)
    
    return {
        'is_deepfake': bool(avg_prediction > 0.5),
        'confidence': float(avg_prediction)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Detect based on file type
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                result = detect_deepfake_image(filepath)
            else:
                result = detect_deepfake_video(filepath)
                
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

# Initialize model
model = load_model()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
import os
import numpy as np
from PIL import Image
import tensorflow as tf

# Load the trained model
MODEL_PATH = "Model/Binary_1_model.h5"  # Path to your trained model file
model = tf.keras.models.load_model(MODEL_PATH)

# Resize size
SIZE = 128

def preprocess_image(image_path):
    """
    Preprocess the input image for the model.
    """
    # Load and resize the image
    image = Image.open(image_path).convert("RGB")
    image = image.resize((SIZE, SIZE))
    image_array = np.array(image) / 255.0  # Normalize
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def postprocess_output(prediction):
    """
    Convert the model's output into a binary mask.
    """
    # Convert prediction to binary mask
    binary_mask = np.where(prediction >= 0.5, 255, 0).astype(np.uint8)
    binary_mask = binary_mask.squeeze()  # Remove unnecessary dimensions
    return Image.fromarray(binary_mask)

def getPrediction(input_path):
    """
    Perform segmentation on the given input image.
    
    Args:
        input_path (str): Path to the input image.

    Returns:
        str: Path to the segmented output image.
    """
    # Preprocess the input image
    preprocessed_image = preprocess_image(input_path)

    # Perform prediction
    prediction = model.predict(preprocessed_image)

    # Postprocess the output
    segmented_image = postprocess_output(prediction)

    # Save the segmented output
    output_path = "static/segmented/segmented_output.png"  # Save to the static folder
    segmented_image.save(output_path)

    return output_path

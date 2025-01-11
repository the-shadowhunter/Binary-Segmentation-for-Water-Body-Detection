from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from main import getPrediction
import os

# Save images to the 'static' folder as Flask serves images from this directory
UPLOAD_FOLDER = 'static/images/'
SEGMENTED_FOLDER = 'static/segmented/'

# Create an app object using the Flask class.
app = Flask(__name__, static_folder="static")

# Add reference fingerprint.
app.secret_key = "secret key"

# Define the upload folder to save images uploaded by the user.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEGMENTED_FOLDER'] = SEGMENTED_FOLDER

# Define the route to be home.
@app.route('/')
def index():
    return render_template('index.html')

# Add Post method to the decorator to allow for form submission.
@app.route('/predict', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)  # Use this werkzeug method to secure filename.
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the prediction (segmented image)
            segmented_path = getPrediction(file_path)

            # Extract filename for segmented image
            segmented_filename = os.path.basename(segmented_path)

            # Generate URLs for the uploaded and segmented images
            uploaded_image_url = url_for('static', filename=f'images/{filename}')
            segmented_image_url = url_for('static', filename=f'segmented/{segmented_filename}')

            # Flash the result and segmented image path
            flash('Segmentation completed!')

            return render_template('index.html', uploaded_image_url=uploaded_image_url, segmented_image_url=segmented_image_url)

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)

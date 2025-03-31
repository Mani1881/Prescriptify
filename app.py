from flask import Flask, render_template, request, redirect, url_for
import pytesseract
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename
from fuzzywuzzy import fuzz  # For better medicine matching

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn’t exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def preprocess_image(image_path):
    """Preprocess the image for OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)  # Increase contrast
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Otsu’s thresholding
    denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    kernel = np.ones((2,2), np.uint8)
    processed = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    return processed

def extract_text(image_path):
    """Extract text from the preprocessed image."""
    processed_image = preprocess_image(image_path)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.png')
    cv2.imwrite(temp_path, processed_image)
    text = pytesseract.image_to_string(processed_image, config='--psm 11')  # Sparse text mode
    print(f"OCR Output: '{text}'")  # Debug
    return text

def parse_medicines(text):
    """Parse medicines from extracted text using fuzzy matching."""
    all_medicines = {
        'paracetamol': {'price': 1.5, 'in_stock': True},
    'dolo': {'price': 2.0, 'in_stock': True},
    'crocin': {'price': 3.0, 'in_stock': True},
    'okacet': {'price': 2.5, 'in_stock': True},
    'aspirin': {'price': 1.8, 'in_stock': True},
    'ibuprofen': {'price': 2.2, 'in_stock': True},
    'cetirizine': {'price': 1.2, 'in_stock': True},
    'montelukast': {'price': 4.5, 'in_stock': False},
    'ranitidine': {'price': 3.5, 'in_stock': True},
    'omeprazole': {'price': 2.8, 'in_stock': True},
    'azithromycin': {'price': 5.0, 'in_stock': False},
    'amoxicillin': {'price': 4.0, 'in_stock': True},
    'metformin': {'price': 3.2, 'in_stock': True},
    'atorvastatin': {'price': 6.5, 'in_stock': False},
    'diclofenac': {'price': 2.7, 'in_stock': True},
    'losartan': {'price': 5.2, 'in_stock': True}
    }
    text = text.lower()
    available_medicines = {}
    for med in all_medicines:
        if fuzz.partial_ratio(med, text) > 80:  # 80% similarity threshold
            available_medicines[med] = all_medicines[med]
    print(f"Parsed Medicines: {available_medicines}")  # Debug
    return available_medicines

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'prescription_image' not in request.files:
            return redirect(request.url)
        file = request.files['prescription_image']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            extracted_text = extract_text(file_path)
            medicines = parse_medicines(extracted_text)
            print(f"Rendering results with order: {medicines}")  # Debug
            return render_template('results.html', patient_name=request.form['patient_name'], order=medicines)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

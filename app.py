from flask import Flask, request, jsonify, send_from_directory, url_for
import os
import random

app = Flask(__name__)
# Define the uploads directory
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    filename = image.filename
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)
    
    return jsonify({"message": "Image uploaded successfully", "filename": filename})

@app.route('/random-image', methods=['GET'])
def random_image():
    images = os.listdir(app.config["UPLOAD_FOLDER"])
    if not images:
        return jsonify({"error": "No images found"}), 404
    
    selected_image = random.choice(images)
    image_url = url_for('uploaded_file', filename=selected_image, _external=True)

    # Return JSON formatted for Farcaster Frames
    return jsonify({
        "title": "Pick an Option",   # Required title
        "description": "Choose A, B, or C",  # Required description
        "image": image_url,
        "buttons": [
            {"label": "A", "action": "post", "target": request.url},
            {"label": "B", "action": "post", "target": request.url},
            {"label": "C", "action": "post", "target": request.url}
        ]
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == '__main__':
    app.run(debug=True)

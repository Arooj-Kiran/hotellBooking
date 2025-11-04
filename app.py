from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder=None, template_folder='templates')

# --- MongoDB connection ---
client = MongoClient("mongodb+srv://aroojk175_db_user:HsESRj3Iq7xGxsEq@cluster0.6veg5kb.mongodb.net/?appName=Cluster0")
db = client["Sample_DB"]
collection = db["Users"]
collection1 = db["Queries"]
# --- Room limits ---
ROOM_LIMIT = {
    "Laxaries Rooms": 10,
    "Deluxe Room": 10,
    "Signature Room": 10,
    "Couple Room": 10
}

# --- Serve static files from inside templates ---
@app.route('/<folder>/<path:filename>')
def serve_static_files(folder, filename):
    allowed_folders = ['css', 'js', 'img', 'images', 'vendor', 'fonts']
    if folder in allowed_folders:
        path = os.path.join(app.template_folder, folder)
        return send_from_directory(path, filename)
    return "File not found", 404


@app.route('/')
def index():
    return render_template('rooms.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# --- Book room ---
@app.route('/Contact', methods=['POST'])
def save_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    if not (name and email and subject and message):
        return jsonify({"status": "error", "message": "Missing contact details"})
    # Save directly to MongoDB   
    collection1.insert_one({
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    })
    return jsonify({"status": "success", "message": "Contact details saved successfully!"})



# --- Book room ---
@app.route('/check-availability', methods=['POST'])
def save_booking():
    room_type = request.form.get('room_type')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')

    if not (room_type and check_in and check_out):
        return jsonify({"status": "error", "message": "Missing booking details"})

    # Save directly to MongoDB   
    collection.insert_one({
        "room_type": room_type,
        "check_in": check_in,
        "check_out": check_out
    })

    return jsonify({"status": "success", "message": "Booking details saved successfully!"})


if __name__ == '__main__':
    app.run(debug=True)

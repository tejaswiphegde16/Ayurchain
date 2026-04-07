from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# Sample data storage (in production, use a real database)
users = {}
plant_records = {}

@app.route('/')
def index():
    """Serve the main index page"""
    return render_template('index.html')

@app.route('/ayurchain')
def ayurchain_page():
    """Serve the AyurChain app page"""
    return render_template('ayurchain.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.json
    username = data.get('username')
    role = data.get('role')
    
    if username and role:
        users[username] = {
            'username': username,
            'role': role,
            'login_time': datetime.now().isoformat()
        }
        return jsonify({
            'success': True,
            'message': f'Welcome {username}!',
            'user': users[username]
        }), 200
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 400

@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    """Get user information"""
    if username in users:
        return jsonify(users[username]), 200
    return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/api/plant', methods=['POST'])
def add_plant():
    """Add a new plant record"""
    data = request.json
    plant_id = data.get('plant_id')
    
    if plant_id:
        plant_records[plant_id] = {
            'plant_id': plant_id,
            'name': data.get('name'),
            'species': data.get('species'),
            'location': data.get('location'),
            'created_at': datetime.now().isoformat()
        }
        return jsonify({
            'success': True,
            'message': 'Plant record created',
            'data': plant_records[plant_id]
        }), 201
    
    return jsonify({'success': False, 'message': 'Invalid plant data'}), 400

@app.route('/api/plant/<plant_id>', methods=['GET'])
def get_plant(plant_id):
    """Get plant record by ID"""
    if plant_id in plant_records:
        return jsonify(plant_records[plant_id]), 200
    return jsonify({'success': False, 'message': 'Plant not found'}), 404

@app.route('/api/plants', methods=['GET'])
def get_all_plants():
    """Get all plant records"""
    return jsonify(list(plant_records.values())), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AyurChain Backend',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("🌿 AyurChain Backend Server Starting...")
    print("📍 Navigate to http://localhost:5000/")
    print("📱 API Documentation available at http://localhost:5000/api/health")
    app.run(debug=True, host='localhost', port=5000)

from flask import Blueprint, request, jsonify
import jwt
import datetime
import os
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Secret key for JWT
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key')

# Mock user database for demo
USERS = {
    'admin': {
        'password': 'admin123',
        'id': 1,
        'role': 'admin'
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = USERS.get(data['username'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': f'Token is invalid! Error: {str(e)}'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/test', methods=['POST'])
def test_auth():
    try:
        # Log request for debugging
        print(f"Auth test request received: {request.method} {request.path}")
        
        # Get request data
        data = request.get_json()
        if not data:
            print("No JSON data in request")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        print(f"Login attempt for user: {username}")
        
        # Simple validation
        if not username or not password:
            print("Missing username or password")
            return jsonify({'success': False, 'message': 'Missing username or password'}), 400
            
        user = USERS.get(username)
        
        if not user or user['password'] != password:
            print(f"Invalid credentials for user: {username}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
        # Generate token
        token = jwt.encode({
            'username': username,
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        
        print(f"Authentication successful for user: {username}")
        
        # Return success response with explicit message and user ID
        return jsonify({
            'success': True,
            'message': 'Authentication successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': username,
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        # Log the error
        print(f"Authentication error: {str(e)}")
        
        # Return error response
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Log request for debugging
        print(f"Login request received: {request.method} {request.path}")
        
        # Get request data
        data = request.get_json()
        if not data:
            print("No JSON data in request")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        print(f"Login attempt for user: {username}")
        
        # Simple validation
        if not username or not password:
            print("Missing username or password")
            return jsonify({'success': False, 'message': 'Missing username or password'}), 400
            
        user = USERS.get(username)
        
        if not user or user['password'] != password:
            print(f"Invalid credentials for user: {username}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
        # Generate token
        token = jwt.encode({
            'username': username,
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        
        print(f"Authentication successful for user: {username}")
        
        # Return success response
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user['id'],
                'username': username,
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        # Log the error
        print(f"Authentication error: {str(e)}")
        
        # Return error response
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Log request for debugging
        print(f"Register request received: {request.method} {request.path}")
        
        # Get request data
        data = request.get_json()
        if not data:
            print("No JSON data in request")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        # Simple validation
        if not username or not password:
            print("Missing username or password")
            return jsonify({'success': False, 'message': 'Missing username or password'}), 400
            
        # Check if user already exists
        if username in USERS:
            print(f"User already exists: {username}")
            return jsonify({'success': False, 'message': 'Username already taken'}), 409
            
        # Create new user (in a real app, this would be saved to a database)
        user_id = len(USERS) + 1
        USERS[username] = {
            'password': password,
            'id': user_id,
            'role': 'user'  # Default role for new users
        }
        
        print(f"User registered successfully: {username}")
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'username': username,
                'role': 'user'
            }
        }), 201
        
    except Exception as e:
        # Log the error
        print(f"Registration error: {str(e)}")
        
        # Return error response
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    try:
        return jsonify({
            'success': True,
            'user': {
                'id': current_user['id'],
                'username': current_user['username'],
                'role': current_user['role']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

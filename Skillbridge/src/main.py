import os
import sys
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Insert the src directory at the beginning of the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
logger.info("Starting SkillBridge backend server...")

# Create Flask app
app = Flask(__name__)
logger.info("Flask app created")

# Configure CORS to allow requests from specific origin with credentials
# Fix for CORS issue with credentials
CORS(app, 
     resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", 
                                   "https://skillbridge-frontend.netlify.app"]}}, 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
logger.info("CORS configured with multiple origins")

# Secret key for JWT
app.config['SECRET_KEY'] = 'skillbridge_secret_key'

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillbridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logger.info("App configuration complete")

# Import and register blueprints
from src.routes.auth import auth_bp
from src.routes.skill import skill_bp

# IMPORTANT: Comment out blueprint registration to avoid route conflicts
# app.register_blueprint(auth_bp, url_prefix='/api/auth')
# app.register_blueprint(skill_bp, url_prefix='/api/skill')
logger.info("Blueprints registration DISABLED to avoid conflicts")

# Root endpoint
@app.route('/')
def index():
    logger.info("Root endpoint accessed")
    return jsonify({
        'message': 'Welcome to SkillBridge API',
        'status': 'online',
        'version': '1.0.0'
    })

# Health check endpoint
@app.route('/api/health')
def health_check():
    logger.info("Health check endpoint accessed")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Debug endpoint to test authentication
@app.route('/api/auth/test', methods=['POST', 'OPTIONS'])
def test_auth():
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request for auth test")
        # Don't use wildcard for Access-Control-Allow-Origin when using credentials
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    logger.info("Auth test endpoint accessed")
    try:
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        username = data.get('username')
        password = data.get('password')
        
        # Log the request for debugging
        logger.info(f"Auth test request received: username={username}, password={'*' * len(password) if password else None}")
        
        # Simple test authentication
        if username == 'admin' and password == 'admin123':
            # Generate JWT token
            token = jwt.encode({
                'sub': username,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=24),
                'user_id': 1,  # Add user_id to token payload
                'role': 'admin'
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            logger.info(f"Authentication successful for user: {username}")
            
            response = jsonify({
                'success': True,
                'message': 'Authentication successful',
                'token': token,
                'user': {
                    'id': 1,  # Adding explicit user ID for admin
                    'username': username,
                    'role': 'admin'
                }
            })
            # Set CORS headers for the main response
            origin = request.headers.get('Origin')
            if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
                response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        else:
            logger.warning(f"Authentication failed for user: {username}")
            response = jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
            return response
    except Exception as e:
        logger.error(f"Error in auth test endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

# Mock data endpoint for dashboard
@app.route('/api/skill/users/<int:user_id>/skills', methods=['GET', 'OPTIONS'])
def mock_user_skills(user_id):
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info(f"Handling OPTIONS request for mock user skills: user_id={user_id}")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info(f"Mock user skills endpoint accessed: user_id={user_id}")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    # Mock data for user skills
    mock_skills = [
        {
            'id': 1,
            'user_id': user_id,
            'skill_id': 1,
            'skill_name': 'Python',
            'proficiency_level': 4,
            'years_experience': 3,
            'is_certified': True,
            'certification_name': 'Python Professional',
            'last_used': '2025-04-01'
        },
        {
            'id': 2,
            'user_id': user_id,
            'skill_id': 2,
            'skill_name': 'JavaScript',
            'proficiency_level': 3,
            'years_experience': 2,
            'is_certified': False,
            'certification_name': None,
            'last_used': '2025-05-01'
        },
        {
            'id': 3,
            'user_id': user_id,
            'skill_id': 3,
            'skill_name': 'React',
            'proficiency_level': 3,
            'years_experience': 1,
            'is_certified': False,
            'certification_name': None,
            'last_used': '2025-05-10'
        }
    ]
    
    response = jsonify({
        'user_skills': mock_skills
    })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# Mock endpoint for skills list
@app.route('/api/skill/skills', methods=['GET', 'OPTIONS'])
def mock_skills():
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request for skills list")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info("Mock skills list endpoint accessed")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    # Mock data for skills
    mock_skills = [
        {
            'id': 1,
            'name': 'Python',
            'category': 'Programming',
            'description': 'Python programming language'
        },
        {
            'id': 2,
            'name': 'JavaScript',
            'category': 'Programming',
            'description': 'JavaScript programming language'
        },
        {
            'id': 3,
            'name': 'React',
            'category': 'Frontend',
            'description': 'React JavaScript library'
        },
        {
            'id': 4,
            'name': 'Flask',
            'category': 'Backend',
            'description': 'Flask Python web framework'
        },
        {
            'id': 5,
            'name': 'SQL',
            'category': 'Database',
            'description': 'SQL database language'
        }
    ]
    
    response = jsonify({
        'skills': mock_skills
    })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# Mock endpoint for projects list
@app.route('/api/skill/projects', methods=['GET', 'OPTIONS'])
def mock_projects():
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request for projects list")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info("Mock projects list endpoint accessed")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    # Mock data for projects
    mock_projects = [
        {
            'id': 1,
            'name': 'SkillBridge Platform',
            'description': 'Development of the SkillBridge platform',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'status': 'active',
            'company_id': 1,
            'member_count': 5
        },
        {
            'id': 2,
            'name': 'AI Interview Coach',
            'description': 'AI-powered interview coaching system',
            'start_date': '2025-02-15',
            'end_date': '2025-08-15',
            'status': 'planning',
            'company_id': 1,
            'member_count': 3
        },
        {
            'id': 3,
            'name': 'NeuroNavi',
            'description': 'Neural navigation system for HR',
            'start_date': '2025-03-01',
            'end_date': '2025-09-30',
            'status': 'active',
            'company_id': 1,
            'member_count': 4
        }
    ]
    
    response = jsonify({
        'projects': mock_projects
    })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# Mock endpoint for skill gap analysis
@app.route('/api/skill/projects/<int:project_id>/skill-gap', methods=['GET', 'OPTIONS'])
def mock_skill_gap(project_id):
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info(f"Handling OPTIONS request for skill gap: project_id={project_id}")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info(f"Mock skill gap endpoint accessed: project_id={project_id}")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    # Mock data for skill gap
    mock_skill_gap = [
        {
            'skill_id': 1,
            'skill_name': 'Python',
            'importance_level': 5,
            'coverage': 2,
            'avg_proficiency': 3.5,
            'gap_score': 1.5
        },
        {
            'skill_id': 2,
            'skill_name': 'JavaScript',
            'importance_level': 4,
            'coverage': 1,
            'avg_proficiency': 3.0,
            'gap_score': 1.0
        },
        {
            'skill_id': 3,
            'skill_name': 'React',
            'importance_level': 4,
            'coverage': 1,
            'avg_proficiency': 3.0,
            'gap_score': 1.0
        },
        {
            'skill_id': 4,
            'skill_name': 'Flask',
            'importance_level': 3,
            'coverage': 1,
            'avg_proficiency': 4.0,
            'gap_score': -1.0
        },
        {
            'skill_id': 5,
            'skill_name': 'SQL',
            'importance_level': 3,
            'coverage': 0,
            'avg_proficiency': 0.0,
            'gap_score': 3.0
        }
    ]
    
    response = jsonify({
        'skill_gap': mock_skill_gap
    })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# Mock endpoint for user profile
@app.route('/api/auth/profile/<int:user_id>', methods=['GET', 'OPTIONS'])
def mock_user_profile(user_id):
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info(f"Handling OPTIONS request for user profile: user_id={user_id}")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info(f"Mock user profile endpoint accessed: user_id={user_id}")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    # Mock data for user profile
    mock_profile = {
        'id': user_id,
        'username': 'admin',
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'admin',
        'company_id': 1,
        'company_name': 'SkillBridge Inc.',
        'job_title': 'System Administrator',
        'department': 'IT',
        'location': 'New York',
        'bio': 'Experienced system administrator with a passion for HR technology.',
        'skills_count': 3,
        'projects_count': 2,
        'joined_date': '2025-01-01'
    }
    
    response = jsonify({
        'profile': mock_profile
    })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# NEW: Mock endpoint for admin users list
@app.route('/api/auth/users', methods=['GET', 'POST', 'OPTIONS'])
def mock_admin_users():
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request for admin users list")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info("Mock admin users endpoint accessed")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    if request.method == 'POST':
        # Handle user creation (just log it, don't actually create)
        data = request.get_json()
        logger.info(f"Received request to create user: {data}")
        
        response = jsonify({
            'success': True,
            'message': 'User created successfully',
            'user_id': 4  # Mock new user ID
        })
    else:
        # Mock data for users list
        mock_users = [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'company_id': 1,
                'is_active': True
            },
            {
                'id': 2,
                'username': 'manager1',
                'email': 'manager1@example.com',
                'first_name': 'John',
                'last_name': 'Manager',
                'role': 'manager',
                'company_id': 1,
                'is_active': True
            },
            {
                'id': 3,
                'username': 'user1',
                'email': 'user1@example.com',
                'first_name': 'Jane',
                'last_name': 'User',
                'role': 'user',
                'company_id': 2,
                'is_active': True
            }
        ]
        
        response = jsonify({
            'users': mock_users
        })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# NEW: Mock endpoint for admin companies list
@app.route('/api/auth/companies', methods=['GET', 'POST', 'OPTIONS'])
def mock_admin_companies():
    # Debug logging for all headers
    logger.debug("==== HEADERS START ====")
    for header, value in request.headers.items():
        logger.debug(f"{header}: {value}")
    logger.debug("==== HEADERS END ====")
    
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request for admin companies list")
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    logger.info("Mock admin companies endpoint accessed")
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header}")
    
    # IMPORTANT: For demo purposes, ALWAYS return mock data regardless of token
    logger.info("BYPASSING TOKEN VALIDATION - Returning mock data for any request")
    
    if request.method == 'POST':
        # Handle company creation (just log it, don't actually create)
        data = request.get_json()
        logger.info(f"Received request to create company: {data}")
        
        response = jsonify({
            'success': True,
            'message': 'Company created successfully',
            'company_id': 4  # Mock new company ID
        })
    else:
        # Mock data for companies list
        mock_companies = [
            {
                'id': 1,
                'name': 'SkillBridge Inc.',
                'industry': 'Technology',
                'size': 'medium',
                'employee_count': 50
            },
            {
                'id': 2,
                'name': 'TechCorp',
                'industry': 'IT Services',
                'size': 'large',
                'employee_count': 200
            },
            {
                'id': 3,
                'name': 'Innovate Solutions',
                'industry': 'Consulting',
                'size': 'small',
                'employee_count': 15
            }
        ]
        
        response = jsonify({
            'companies': mock_companies
        })
    
    # Set CORS headers for the main response
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response

# Run the app
if __name__ == '__main__':
    logger.info("Starting Flask server on port 5002")
    app.run(host='0.0.0.0', port=5002, debug=True)

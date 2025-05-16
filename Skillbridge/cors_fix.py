// CORS configuration fix for SkillBridge backend
// Add this to the main.py file in the create_app function

from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configure CORS to allow requests from the frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    # Rest of the app configuration...

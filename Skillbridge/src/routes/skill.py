from flask import Blueprint, request, jsonify
from src.models.skill import db, Skill, UserSkill, Project, ProjectMember, ProjectSkill
import jwt
import os
from datetime import datetime

skill_bp = Blueprint('skill', __name__)

# Secret key for JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Helper function to verify JWT token
def verify_token(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {'error': 'Authorization token is missing'}, 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload, None, None
    
    except jwt.ExpiredSignatureError:
        return None, {'error': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return None, {'error': 'Invalid token'}, 401

# Skill management endpoints
@skill_bp.route('/skills', methods=['GET'])
def get_skills():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get query parameters for filtering
    category = request.args.get('category')
    
    # Build query
    query = Skill.query
    
    if category:
        query = query.filter_by(category=category)
    
    # Execute query
    skills = query.all()
    
    return jsonify({
        'skills': [skill.to_dict() for skill in skills]
    }), 200

@skill_bp.route('/skills', methods=['POST'])
def create_skill():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin
    if payload['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Skill name is required'}), 400
    
    # Check if skill already exists
    if Skill.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Skill already exists'}), 409
    
    # Create new skill
    new_skill = Skill(
        name=data['name'],
        category=data.get('category'),
        description=data.get('description')
    )
    
    # Save to database
    db.session.add(new_skill)
    db.session.commit()
    
    return jsonify({
        'message': 'Skill created successfully',
        'skill': new_skill.to_dict()
    }), 201

@skill_bp.route('/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get skill from database
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    return jsonify({
        'skill': skill.to_dict()
    }), 200

@skill_bp.route('/skills/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin
    if payload['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get skill from database
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    data = request.get_json()
    
    # Update skill data
    if 'name' in data:
        skill.name = data['name']
    if 'category' in data:
        skill.category = data['category']
    if 'description' in data:
        skill.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Skill updated successfully',
        'skill': skill.to_dict()
    }), 200

@skill_bp.route('/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin
    if payload['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get skill from database
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    # Delete skill
    db.session.delete(skill)
    db.session.commit()
    
    return jsonify({
        'message': 'Skill deleted successfully'
    }), 200

# User skill management endpoints
@skill_bp.route('/users/<int:user_id>/skills', methods=['GET'])
def get_user_skills(user_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin or the user themselves
    if payload['role'] != 'admin' and payload['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get user skills
    user_skills = UserSkill.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'user_skills': [user_skill.to_dict() for user_skill in user_skills]
    }), 200

@skill_bp.route('/users/<int:user_id>/skills', methods=['POST'])
def add_user_skill(user_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin or the user themselves
    if payload['role'] != 'admin' and payload['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('skill_id'):
        return jsonify({'error': 'Skill ID is required'}), 400
    
    # Check if skill exists
    skill = Skill.query.get(data['skill_id'])
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    # Check if user already has this skill
    existing_skill = UserSkill.query.filter_by(
        user_id=user_id,
        skill_id=data['skill_id']
    ).first()
    
    if existing_skill:
        return jsonify({'error': 'User already has this skill'}), 409
    
    # Create new user skill
    new_user_skill = UserSkill(
        user_id=user_id,
        skill_id=data['skill_id'],
        proficiency_level=data.get('proficiency_level', 1),
        years_experience=data.get('years_experience'),
        is_certified=data.get('is_certified', False),
        certification_name=data.get('certification_name'),
        certification_date=datetime.strptime(data['certification_date'], '%Y-%m-%d').date() if data.get('certification_date') else None,
        last_used=datetime.strptime(data['last_used'], '%Y-%m-%d').date() if data.get('last_used') else None
    )
    
    # Save to database
    db.session.add(new_user_skill)
    db.session.commit()
    
    return jsonify({
        'message': 'User skill added successfully',
        'user_skill': new_user_skill.to_dict()
    }), 201

# Project management endpoints
@skill_bp.route('/projects', methods=['GET'])
def get_projects():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get query parameters for filtering
    company_id = request.args.get('company_id', type=int)
    status = request.args.get('status')
    
    # Build query
    query = Project.query
    
    if company_id:
        query = query.filter_by(company_id=company_id)
    
    if status:
        query = query.filter_by(status=status)
    
    # Execute query
    projects = query.all()
    
    return jsonify({
        'projects': [project.to_dict() for project in projects]
    }), 200

@skill_bp.route('/projects', methods=['POST'])
def create_project():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin or manager
    if payload['role'] not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'company_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new project
    new_project = Project(
        name=data['name'],
        description=data.get('description'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
        status=data.get('status', 'planning'),
        company_id=data['company_id']
    )
    
    # Save to database
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({
        'message': 'Project created successfully',
        'project': new_project.to_dict()
    }), 201

@skill_bp.route('/projects/<int:project_id>/skills', methods=['GET'])
def get_project_skills(project_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get project skills
    project_skills = ProjectSkill.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'project_skills': [project_skill.to_dict() for project_skill in project_skills]
    }), 200

@skill_bp.route('/projects/<int:project_id>/skills', methods=['POST'])
def add_project_skill(project_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin or manager
    if payload['role'] not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('skill_id'):
        return jsonify({'error': 'Skill ID is required'}), 400
    
    # Check if skill exists
    skill = Skill.query.get(data['skill_id'])
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    # Check if project exists
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Check if project already has this skill
    existing_skill = ProjectSkill.query.filter_by(
        project_id=project_id,
        skill_id=data['skill_id']
    ).first()
    
    if existing_skill:
        return jsonify({'error': 'Project already has this skill'}), 409
    
    # Create new project skill
    new_project_skill = ProjectSkill(
        project_id=project_id,
        skill_id=data['skill_id'],
        importance_level=data.get('importance_level', 3)
    )
    
    # Save to database
    db.session.add(new_project_skill)
    db.session.commit()
    
    return jsonify({
        'message': 'Project skill added successfully',
        'project_skill': new_project_skill.to_dict()
    }), 201

# Skill gap analysis endpoint
@skill_bp.route('/projects/<int:project_id>/skill-gap', methods=['GET'])
def analyze_skill_gap(project_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if project exists
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get project skills
    project_skills = ProjectSkill.query.filter_by(project_id=project_id).all()
    
    # Get project members
    project_members = ProjectMember.query.filter_by(project_id=project_id).all()
    
    # Get user skills for all project members
    user_skills = []
    for member in project_members:
        member_skills = UserSkill.query.filter_by(user_id=member.user_id).all()
        user_skills.extend(member_skills)
    
    # Analyze skill gap
    skill_gap = []
    for project_skill in project_skills:
        # Find matching user skills
        matching_skills = [us for us in user_skills if us.skill_id == project_skill.skill_id]
        
        # Calculate coverage
        coverage = len(matching_skills)
        
        # Calculate average proficiency
        avg_proficiency = sum(us.proficiency_level for us in matching_skills) / len(matching_skills) if matching_skills else 0
        
        skill_gap.append({
            'skill_id': project_skill.skill_id,
            'skill_name': project_skill.skill.name,
            'importance_level': project_skill.importance_level,
            'coverage': coverage,
            'avg_proficiency': avg_proficiency,
            'gap_score': project_skill.importance_level - (avg_proficiency * coverage / len(project_members) if project_members else 0)
        })
    
    # Sort by gap score (highest first)
    skill_gap.sort(key=lambda x: x['gap_score'], reverse=True)
    
    return jsonify({
        'project_id': project_id,
        'project_name': project.name,
        'skill_gap': skill_gap
    }), 200

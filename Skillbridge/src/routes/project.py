from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.skill import Project, ProjectMember
import jwt
import os
from datetime import datetime

project_bp = Blueprint('project', __name__)

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

# User projects endpoints
@project_bp.route('/users/<int:user_id>/projects', methods=['GET'])
def get_user_projects(user_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin or the user themselves
    if payload['role'] != 'admin' and payload['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get user's project memberships
    memberships = ProjectMember.query.filter_by(user_id=user_id).all()
    
    # Get projects from memberships
    projects = []
    for membership in memberships:
        project = Project.query.get(membership.project_id)
        if project:
            project_dict = project.to_dict()
            project_dict['role'] = membership.role
            project_dict['allocation'] = membership.allocation_percentage
            project_dict['joined_date'] = membership.joined_date.isoformat() if membership.joined_date else None
            projects.append(project_dict)
    
    return jsonify({
        'projects': projects
    }), 200

@project_bp.route('/projects/<int:project_id>/members', methods=['GET'])
def get_project_members(project_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get project
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get project memberships
    memberships = ProjectMember.query.filter_by(project_id=project_id).all()
    
    # Get members with details
    members = []
    for membership in memberships:
        user = User.query.get(membership.user_id)
        if user:
            member = {
                'id': membership.id,
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': membership.role,
                'allocation_percentage': membership.allocation_percentage,
                'joined_date': membership.joined_date.isoformat() if membership.joined_date else None
            }
            members.append(member)
    
    return jsonify({
        'members': members
    }), 200

@project_bp.route('/projects/<int:project_id>/members', methods=['POST'])
def add_project_member(project_id):
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
    if not data.get('user_id'):
        return jsonify({'error': 'User ID is required'}), 400
    
    # Check if project exists
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user is already a member
    existing_membership = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=data['user_id']
    ).first()
    
    if existing_membership:
        return jsonify({'error': 'User is already a member of this project'}), 409
    
    # Create new project membership
    new_membership = ProjectMember(
        project_id=project_id,
        user_id=data['user_id'],
        role=data.get('role'),
        allocation_percentage=data.get('allocation_percentage', 100),
        joined_date=datetime.strptime(data['joined_date'], '%Y-%m-%d').date() if data.get('joined_date') else datetime.now().date()
    )
    
    # Save to database
    db.session.add(new_membership)
    db.session.commit()
    
    return jsonify({
        'message': 'Project member added successfully',
        'membership': new_membership.to_dict()
    }), 201

@project_bp.route('/projects/<int:project_id>/members/<int:membership_id>', methods=['DELETE'])
def remove_project_member(project_id, membership_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin or manager
    if payload['role'] not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Check if project exists
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Check if membership exists
    membership = ProjectMember.query.get(membership_id)
    if not membership or membership.project_id != project_id:
        return jsonify({'error': 'Project membership not found'}), 404
    
    # Delete membership
    db.session.delete(membership)
    db.session.commit()
    
    return jsonify({
        'message': 'Project member removed successfully'
    }), 200

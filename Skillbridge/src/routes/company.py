from flask import Blueprint, request, jsonify
from src.models.user import db, Company
import jwt
import os

company_bp = Blueprint('company', __name__)

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

# Company management endpoints
@company_bp.route('/companies', methods=['GET'])
def get_companies():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get all companies
    companies = Company.query.all()
    
    return jsonify({
        'companies': [company.to_dict() for company in companies]
    }), 200

@company_bp.route('/companies', methods=['POST'])
def create_company():
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
        return jsonify({'error': 'Company name is required'}), 400
    
    # Create new company
    new_company = Company(
        name=data['name'],
        industry=data.get('industry'),
        size=data.get('size', 'medium')
    )
    
    # Save to database
    db.session.add(new_company)
    db.session.commit()
    
    return jsonify({
        'message': 'Company created successfully',
        'company': new_company.to_dict()
    }), 201

@company_bp.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Get company from database
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    return jsonify({
        'company': company.to_dict()
    }), 200

@company_bp.route('/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin
    if payload['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get company from database
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    data = request.get_json()
    
    # Update company data
    if 'name' in data:
        company.name = data['name']
    if 'industry' in data:
        company.industry = data['industry']
    if 'size' in data:
        company.size = data['size']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Company updated successfully',
        'company': company.to_dict()
    }), 200

@company_bp.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    payload, error, status_code = verify_token(auth_header)
    
    if error:
        return jsonify(error), status_code
    
    # Check if user is admin
    if payload['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get company from database
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    # Check if company has employees
    if company.employees and len(company.employees) > 0:
        return jsonify({'error': 'Cannot delete company with employees'}), 400
    
    # Delete company
    db.session.delete(company)
    db.session.commit()
    
    return jsonify({
        'message': 'Company deleted successfully'
    }), 200

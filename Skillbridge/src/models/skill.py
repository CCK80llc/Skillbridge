from flask_sqlalchemy import SQLAlchemy
from src.models.user import db, User
from datetime import datetime

# Skill model
class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# UserSkill model (association between User and Skill)
class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    proficiency_level = db.Column(db.Integer)  # 1-5
    years_experience = db.Column(db.Float)
    is_certified = db.Column(db.Boolean, default=False)
    certification_name = db.Column(db.String(100))
    certification_date = db.Column(db.Date)
    last_used = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define relationships
    user = db.relationship('User', backref=db.backref('skills', lazy=True))
    skill = db.relationship('Skill', backref=db.backref('users', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_id': self.skill_id,
            'skill_name': self.skill.name if self.skill else None,
            'proficiency_level': self.proficiency_level,
            'years_experience': self.years_experience,
            'is_certified': self.is_certified,
            'certification_name': self.certification_name,
            'certification_date': self.certification_date.isoformat() if self.certification_date else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Project model
class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='planning')  # planning, active, completed, on-hold
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define relationship with Company
    company = db.relationship('Company', backref=db.backref('projects', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'member_count': len(self.members) if hasattr(self, 'members') else 0
        }

# ProjectMember model (association between Project and User)
class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50))  # Developer, Designer, Manager, etc.
    allocation_percentage = db.Column(db.Integer, default=100)
    joined_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    project = db.relationship('Project', backref=db.backref('members', lazy=True))
    user = db.relationship('User', backref=db.backref('projects', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'role': self.role,
            'allocation_percentage': self.allocation_percentage,
            'joined_date': self.joined_date.isoformat() if self.joined_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ProjectSkill model (association between Project and Skill)
class ProjectSkill(db.Model):
    __tablename__ = 'project_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    importance_level = db.Column(db.Integer)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    project = db.relationship('Project', backref=db.backref('skills', lazy=True))
    skill = db.relationship('Skill', backref=db.backref('projects', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'skill_id': self.skill_id,
            'skill_name': self.skill.name if self.skill else None,
            'importance_level': self.importance_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

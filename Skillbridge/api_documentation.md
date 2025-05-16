# API Documentation for SkillBridge SaaS Platform

## Base URL
```
http://localhost:5000/api
```

## Authentication Endpoints

### Register a new user
- **URL**: `/auth/register`
- **Method**: `POST`
- **Auth required**: No
- **Request body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"  // Optional, defaults to "user"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "company_id": null,
      "created_at": "2025-05-15T22:00:00.000Z",
      "last_login": null,
      "is_active": true
    }
  }
  ```

### Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Auth required**: No
- **Request body**:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "company_id": null,
      "created_at": "2025-05-15T22:00:00.000Z",
      "last_login": "2025-05-15T22:05:00.000Z",
      "is_active": true
    }
  }
  ```

### Get User Profile
- **URL**: `/auth/profile`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "company_id": null,
      "created_at": "2025-05-15T22:00:00.000Z",
      "last_login": "2025-05-15T22:05:00.000Z",
      "is_active": true
    }
  }
  ```

### Update User Profile
- **URL**: `/auth/profile`
- **Method**: `PUT`
- **Auth required**: Yes (Bearer Token)
- **Request body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "password": "newsecurepassword"  // Optional
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Profile updated successfully",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john.smith@example.com",
      "first_name": "John",
      "last_name": "Smith",
      "role": "user",
      "company_id": null,
      "created_at": "2025-05-15T22:00:00.000Z",
      "last_login": "2025-05-15T22:05:00.000Z",
      "is_active": true
    }
  }
  ```

## Skills Management Endpoints

### Get All Skills
- **URL**: `/skill/skills`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Query Parameters**:
  - `category` (optional): Filter skills by category
- **Success Response**: `200 OK`
  ```json
  {
    "skills": [
      {
        "id": 1,
        "name": "JavaScript",
        "category": "Programming",
        "description": "A programming language for the web",
        "created_at": "2025-05-15T22:00:00.000Z"
      },
      {
        "id": 2,
        "name": "Python",
        "category": "Programming",
        "description": "A versatile programming language",
        "created_at": "2025-05-15T22:00:00.000Z"
      }
    ]
  }
  ```

### Create a New Skill
- **URL**: `/skill/skills`
- **Method**: `POST`
- **Auth required**: Yes (Bearer Token with admin role)
- **Request body**:
  ```json
  {
    "name": "React",
    "category": "Frontend",
    "description": "A JavaScript library for building user interfaces"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "Skill created successfully",
    "skill": {
      "id": 3,
      "name": "React",
      "category": "Frontend",
      "description": "A JavaScript library for building user interfaces",
      "created_at": "2025-05-15T22:10:00.000Z"
    }
  }
  ```

### Get User Skills
- **URL**: `/skill/users/{user_id}/skills`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "user_skills": [
      {
        "id": 1,
        "user_id": 1,
        "skill_id": 1,
        "skill_name": "JavaScript",
        "proficiency_level": 4,
        "years_experience": 3.5,
        "is_certified": true,
        "certification_name": "JavaScript Developer Certification",
        "certification_date": "2024-01-15",
        "last_used": "2025-05-01",
        "created_at": "2025-05-15T22:15:00.000Z",
        "updated_at": "2025-05-15T22:15:00.000Z"
      }
    ]
  }
  ```

### Add User Skill
- **URL**: `/skill/users/{user_id}/skills`
- **Method**: `POST`
- **Auth required**: Yes (Bearer Token)
- **Request body**:
  ```json
  {
    "skill_id": 2,
    "proficiency_level": 3,
    "years_experience": 2.0,
    "is_certified": false
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "User skill added successfully",
    "user_skill": {
      "id": 2,
      "user_id": 1,
      "skill_id": 2,
      "skill_name": "Python",
      "proficiency_level": 3,
      "years_experience": 2.0,
      "is_certified": false,
      "certification_name": null,
      "certification_date": null,
      "last_used": null,
      "created_at": "2025-05-15T22:20:00.000Z",
      "updated_at": "2025-05-15T22:20:00.000Z"
    }
  }
  ```

## Project Management Endpoints

### Get All Projects
- **URL**: `/skill/projects`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Query Parameters**:
  - `company_id` (optional): Filter projects by company
  - `status` (optional): Filter projects by status
- **Success Response**: `200 OK`
  ```json
  {
    "projects": [
      {
        "id": 1,
        "name": "Website Redesign",
        "description": "Redesign company website with modern UI",
        "start_date": "2025-06-01",
        "end_date": "2025-08-31",
        "status": "planning",
        "company_id": 1,
        "created_at": "2025-05-15T22:25:00.000Z",
        "updated_at": "2025-05-15T22:25:00.000Z",
        "member_count": 3
      }
    ]
  }
  ```

### Create a New Project
- **URL**: `/skill/projects`
- **Method**: `POST`
- **Auth required**: Yes (Bearer Token with admin or manager role)
- **Request body**:
  ```json
  {
    "name": "Mobile App Development",
    "description": "Develop a mobile app for customers",
    "start_date": "2025-07-01",
    "end_date": "2025-10-31",
    "status": "planning",
    "company_id": 1
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "Project created successfully",
    "project": {
      "id": 2,
      "name": "Mobile App Development",
      "description": "Develop a mobile app for customers",
      "start_date": "2025-07-01",
      "end_date": "2025-10-31",
      "status": "planning",
      "company_id": 1,
      "created_at": "2025-05-15T22:30:00.000Z",
      "updated_at": "2025-05-15T22:30:00.000Z",
      "member_count": 0
    }
  }
  ```

### Get Project Skills
- **URL**: `/skill/projects/{project_id}/skills`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "project_skills": [
      {
        "id": 1,
        "project_id": 1,
        "skill_id": 1,
        "skill_name": "JavaScript",
        "importance_level": 5,
        "created_at": "2025-05-15T22:35:00.000Z"
      },
      {
        "id": 2,
        "project_id": 1,
        "skill_id": 3,
        "skill_name": "React",
        "importance_level": 4,
        "created_at": "2025-05-15T22:35:00.000Z"
      }
    ]
  }
  ```

### Add Project Skill
- **URL**: `/skill/projects/{project_id}/skills`
- **Method**: `POST`
- **Auth required**: Yes (Bearer Token with admin or manager role)
- **Request body**:
  ```json
  {
    "skill_id": 2,
    "importance_level": 3
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "Project skill added successfully",
    "project_skill": {
      "id": 3,
      "project_id": 1,
      "skill_id": 2,
      "skill_name": "Python",
      "importance_level": 3,
      "created_at": "2025-05-15T22:40:00.000Z"
    }
  }
  ```

### Skill Gap Analysis
- **URL**: `/skill/projects/{project_id}/skill-gap`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "project_id": 1,
    "project_name": "Website Redesign",
    "skill_gap": [
      {
        "skill_id": 3,
        "skill_name": "React",
        "importance_level": 4,
        "coverage": 1,
        "avg_proficiency": 3.0,
        "gap_score": 3.0
      },
      {
        "skill_id": 1,
        "skill_name": "JavaScript",
        "importance_level": 5,
        "coverage": 2,
        "avg_proficiency": 4.0,
        "gap_score": 2.33
      },
      {
        "skill_id": 2,
        "skill_name": "Python",
        "importance_level": 3,
        "coverage": 1,
        "avg_proficiency": 3.0,
        "gap_score": 2.0
      }
    ]
  }
  ```

## Company Management Endpoints

### Get All Companies
- **URL**: `/auth/companies`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "companies": [
      {
        "id": 1,
        "name": "Default Company",
        "industry": "Technology",
        "size": "medium",
        "created_at": "2025-05-15T22:00:00.000Z",
        "employee_count": 5
      }
    ]
  }
  ```

### Create a New Company
- **URL**: `/auth/companies`
- **Method**: `POST`
- **Auth required**: Yes (Bearer Token with admin role)
- **Request body**:
  ```json
  {
    "name": "Acme Corporation",
    "industry": "Manufacturing",
    "size": "large"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "Company created successfully",
    "company": {
      "id": 2,
      "name": "Acme Corporation",
      "industry": "Manufacturing",
      "size": "large",
      "created_at": "2025-05-15T22:45:00.000Z",
      "employee_count": 0
    }
  }
  ```

## Project Members Endpoints

### Get Project Members
- **URL**: `/skill/projects/{project_id}/members`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "members": [
      {
        "id": 1,
        "user_id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Smith",
        "role": "Developer",
        "allocation_percentage": 100,
        "joined_date": "2025-05-15"
      }
    ]
  }
  ```

### Add Project Member
- **URL**: `/skill/projects/{project_id}/members`
- **Method**: `POST`
- **Auth required**: Yes (Bearer Token with admin or manager role)
- **Request body**:
  ```json
  {
    "user_id": 2,
    "role": "Designer",
    "allocation_percentage": 50,
    "joined_date": "2025-05-16"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "Project member added successfully",
    "membership": {
      "id": 2,
      "project_id": 1,
      "user_id": 2,
      "role": "Designer",
      "allocation_percentage": 50,
      "joined_date": "2025-05-16",
      "created_at": "2025-05-15T22:50:00.000Z"
    }
  }
  ```

### Get User Projects
- **URL**: `/skill/users/{user_id}/projects`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token)
- **Success Response**: `200 OK`
  ```json
  {
    "projects": [
      {
        "id": 1,
        "name": "Website Redesign",
        "description": "Redesign company website with modern UI",
        "start_date": "2025-06-01",
        "end_date": "2025-08-31",
        "status": "planning",
        "company_id": 1,
        "created_at": "2025-05-15T22:25:00.000Z",
        "updated_at": "2025-05-15T22:25:00.000Z",
        "role": "Developer",
        "allocation": 100,
        "joined_date": "2025-05-15"
      }
    ]
  }
  ```

## Admin Endpoints

### Get All Users
- **URL**: `/auth/users`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token with admin role)
- **Success Response**: `200 OK`
  ```json
  {
    "users": [
      {
        "id": 1,
        "username": "johndoe",
        "email": "john.smith@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "role": "user",
        "company_id": 1,
        "created_at": "2025-05-15T22:00:00.000Z",
        "last_login": "2025-05-15T22:05:00.000Z",
        "is_active": true
      },
      {
        "id": 2,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "company_id": 1,
        "created_at": "2025-05-15T22:00:00.000Z",
        "last_login": "2025-05-15T22:05:00.000Z",
        "is_active": true
      }
    ]
  }
  ```

### Get User by ID
- **URL**: `/auth/users/{user_id}`
- **Method**: `GET`
- **Auth required**: Yes (Bearer Token with admin role or the user themselves)
- **Success Response**: `200 OK`
  ```json
  {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john.smith@example.com",
      "first_name": "John",
      "last_name": "Smith",
      "role": "user",
      "company_id": 1,
      "created_at": "2025-05-15T22:00:00.000Z",
      "last_login": "2025-05-15T22:05:00.000Z",
      "is_active": true
    }
  }
  ```

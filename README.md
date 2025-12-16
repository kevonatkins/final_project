# Final Project – FastAPI Web Application

## Overview
This project is a full-stack FastAPI web application that demonstrates secure authentication, database integration, and automated testing.  
The final project feature adds a **User Profile Password Change** workflow, allowing authenticated users to securely update their password using hashed credentials.

The application is built using:
- FastAPI for backend REST APIs
- SQLAlchemy for database management
- JWT-based authentication and authorization
- Playwright for end-to-end (E2E) testing
- Docker and GitHub Actions for CI/CD automation

---

## Final Project Feature: User Profile & Password Change
This project implements a secure **password change feature** that allows authenticated users to update their password through a profile page.

### Feature Workflow
- User registers and logs in
- User navigates to the profile page
- User submits current password and new password
- Password is securely hashed and updated in the database
- User can log in again using the new password

### Security Implementation
- Passwords are hashed before storage
- Current password verification is required before updating
- JWT tokens protect all sensitive routes
- Unauthorized access is properly rejected

---

## Running the Application

### Run Locally (Without Docker)
```bash
uvicorn app.main:app --reload

```

Application will be available at:

```bash
http://127.0.0.1:8000
```
## Run Using Docker
```bash
docker compose up --build
``` 
## Running Tests
All tests can be executed locally using:
```
pytest
```
## Testing Strategy
- Unit Tests validate password update logic and schemas

- Integration Tests verify database updates and API routes

- End-to-End Tests (Playwright) confirm the full workflow from login to password change and re-login

All tests pass successfully as part of the CI pipeline.

```bash
API Endpoints
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Authenticate user and receive JWT
PUT	/users/me/password	Change authenticated user password
GET	/health	Health check endpoint
``` 
## CI/CD Pipeline
This project uses GitHub Actions to automate:

- Running all unit, integration, and E2E tests

- Building the Docker image after successful tests

- Ensuring code quality before deployment

## Docker Hub Repository
Docker image for this project is available at:


https://hub.docker.com/r/kevonatkins/final_project
## GitHub Repository
Source code and tests are available at:


https://github.com/kevonatkins/final_project
## Learning Outcomes Addressed
- Create Python applications with automated testing

- Build secure REST APIs using FastAPI

- Implement JWT-based authentication and password hashing

- Integrate SQL databases using SQLAlchemy

- Containerize applications using Docker

- Automate testing and deployment using GitHub Actions
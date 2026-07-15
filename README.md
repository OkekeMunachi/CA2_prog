## Project Overview

This project is a REST API built using Python and Flask for managing software issues and security vulnerabilities within ACME Technologies.

The system allows users to:

- Create issues
- View issues
- Update issues
- Delete issues
- Track vulnerabilities
- Search and filter records
- Generate summary reports


## API Endpoints

### Issues
- POST /issues
- GET /issues
- GET /issues/<id>
- PUT /issues/<id>
- DELETE /issues/<id>

### Vulnerabilities
- POST /vulnerabilities
- GET /vulnerabilities
- GET /vulnerabilities/<id>
- PUT /vulnerabilities/<id>
- DELETE /vulnerabilities/<id>

### Reports
- GET /reports/summary

## Attribution Summary

| Component | Source |
|-----------|--------|
| Flask Framework | Flask Documentation |
| SQLAlchemy ORM | Flask-SQLAlchemy Documentation |
| Business Logic | Self |
| API Testing | Self |

## Technologies

- Python
- Flask
- SQLite
- SQLAlchemy
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

## Technologies

- Python
- Flask
- SQLite
- SQLAlchemy
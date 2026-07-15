from flask import jsonify, request
from app.database import db
from app.models import Issue, Vulnerability

VALID_STATUSES = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]

VALID_PRIORITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

VALID_SEVERITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

def register_routes(app):

    # Home Route
    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to ACME Technologies Issue Tracker API"
        })

    # CREATE ISSUE
    @app.route("/issues", methods=["POST"])
    def create_issue():

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        if "title" not in data:
            return jsonify({
                "error": "Title is required"
            }), 400

        if "description" not in data:
            return jsonify({
                "error": "Description is required"
            }), 400

        status = data.get("status", "Open")
        priority=data.get("priority", "Medium"),
        vulnerability_id=data.get("vulnerability_id")

        if status not in VALID_STATUSES:
            return jsonify({
                "error": f"Status must be one of {VALID_STATUSES}"
            }), 400

        if priority not in VALID_PRIORITIES:
            return jsonify({
                "error": f"Priority must be one of {VALID_PRIORITIES}"
            }), 400

        issue = Issue(
            title=data["title"],
            description=data["description"],
            status=status,
            priority=priority
        )

        db.session.add(issue)
        db.session.commit()

        return jsonify({
            "message": "Issue created successfully",
            "issue_id": issue.id
        }), 201

          # READ ALL Issues with filtering, searching and sorting
    @app.route("/issues", methods=["GET"])
    def get_issues():

        status_filter = request.args.get("status")
        priority_filter = request.args.get("priority")
        search_term = request.args.get("search")
        sort_order = request.args.get("sort")

        query = Issue.query

        # Filter by status
        if status_filter:
            query = query.filter_by(status=status_filter)

        # Filter by priority
        if priority_filter:
            query = query.filter_by(priority=priority_filter)

        # Search by title
        if search_term:
            query = query.filter(
                Issue.title.contains(search_term)
            )

        # Sort results
        if sort_order == "priority":
            query = query.order_by(Issue.priority)

        elif sort_order == "status":
            query = query.order_by(Issue.status)

        issues = query.all()

        issue_list = []

        for issue in issues:
            issue_list.append({
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status,
                "priority": issue.priority
            })

        return jsonify(issue_list), 200
        
    # READ ONE Issue
    @app.route("/issues/<int:issue_id>", methods=["GET"])
    def get_issue(issue_id):

        issue = Issue.query.get(issue_id)

        if issue is None:
            return jsonify({
                "error": f"Issue with ID {issue_id} was not found"
                }), 404

        return jsonify({
            "id": issue.id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status,
            "priority": issue.priority
        }), 200

    # UPDATE Issue
    @app.route("/issues/<int:issue_id>", methods=["PUT"])
    def update_issue(issue_id):

        issue = Issue.query.get(issue_id)

        if issue is None:
            return jsonify({
                "error": f"Issue with ID {issue_id} was not found"
                }), 404

        data = request.get_json()

         # Validation 
        if not data:
            return jsonify({
                "error": "Request body is required"
                }), 400

        issue.title = data.get("title", issue.title)
        issue.description = data.get("description", issue.description)
        issue.status = data.get("status", issue.status)
        issue.priority = data.get("priority", issue.priority)

        db.session.commit()

        return jsonify({
            "message": "Issue updated successfully",
            "issue": {
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status,
                "priority": issue.priority
            }
        }), 200

    # DELETE Issue
    @app.route("/issues/<int:issue_id>", methods=["DELETE"])
    def delete_issue(issue_id):

        issue = Issue.query.get(issue_id)

        if issue is None:
            return jsonify({
                "error": f"Issue with ID {issue_id} was not found"
                }), 404

        db.session.delete(issue)
        db.session.commit()

        return jsonify({
            "message": "Issue deleted successfully"
        }), 200

    # CREATE Vulnerability
    @app.route("/vulnerabilities", methods=["POST"])
    def create_vulnerability():

        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400
        
        if "title" not in data:
            return jsonify({
                "error": "Title is required"
            }), 400

        if "description" not in data:
            return jsonify({
                "error": "Description is required"
            }), 400

        severity = data.get("severity", "Medium")

        if severity not in VALID_SEVERITIES:
            return jsonify({
                "error": f"Severity must be one of {VALID_SEVERITIES}"
                }), 400

        vulnerability = Vulnerability(
            title=data["title"],
            description=data["description"],
            severity=data.get("severity", "Medium"),
            cve_id=data.get("cve_id")
        )

        db.session.add(vulnerability)
        db.session.commit()

        return jsonify({
            "message": "Vulnerability created successfully",
            "vulnerability_id": vulnerability.id
        }), 201

         # READ ALL Vulnerabilities with filtering and search
    @app.route("/vulnerabilities", methods=["GET"])
    def get_vulnerabilities():

        severity_filter = request.args.get("severity")
        search_term = request.args.get("search")

        query = Vulnerability.query

        # Filter by severity
        if severity_filter:
            query = query.filter_by(severity=severity_filter)

        # Search by title
        if search_term:
            query = query.filter(
                Vulnerability.title.contains(search_term)
            )

        vulnerabilities = query.all()

        vulnerability_list = []

        for vulnerability in vulnerabilities:
            vulnerability_list.append({
                "id": vulnerability.id,
                "title": vulnerability.title,
                "description": vulnerability.description,
                "severity": vulnerability.severity,
                "cve_id": vulnerability.cve_id
            })

        return jsonify(vulnerability_list), 200

    
    # READ ONE Vulnerability
    @app.route("/vulnerabilities/<int:vulnerability_id>", methods=["GET"])
    def get_vulnerability(vulnerability_id):

        vulnerability = Vulnerability.query.get(vulnerability_id)

        if vulnerability is None:
            return jsonify({
                "error": f"Vulnerability with ID {vulnerability_id} was not found"
            }), 404

        return jsonify({
            "id": vulnerability.id,
            "title": vulnerability.title,
            "description": vulnerability.description,
            "severity": vulnerability.severity,
            "cve_id": vulnerability.cve_id
        }), 200

     # UPDATE Vulnerability
    @app.route("/vulnerabilities/<int:vulnerability_id>", methods=["PUT"])
    def update_vulnerability(vulnerability_id):

        vulnerability = Vulnerability.query.get(vulnerability_id)

        if vulnerability is None:
            return jsonify({
                "error": f"Vulnerability with ID {vulnerability_id} was not found"
            }), 404

        data = request.get_json()

        vulnerability.title = data.get("title", vulnerability.title)
        vulnerability.description = data.get("description", vulnerability.description)
        vulnerability.severity = data.get("severity", vulnerability.severity)
        vulnerability.cve_id = data.get("cve_id", vulnerability.cve_id)

        db.session.commit()

        return jsonify({
            "message": "Vulnerability updated successfully"
        }), 200

        # DELETE Vulnerability
    @app.route("/vulnerabilities/<int:vulnerability_id>", methods=["DELETE"])
    def delete_vulnerability(vulnerability_id):

        vulnerability = Vulnerability.query.get(vulnerability_id)

        if vulnerability is None:
            return jsonify({
                "error": f"Vulnerability with ID {vulnerability_id} was not found"
            }), 404

        db.session.delete(vulnerability)
        db.session.commit()

        return jsonify({
            "message": "Vulnerability deleted successfully"
        }), 200

         
        # Reporting Dashboard
    @app.route("/reports/summary", methods=["GET"])
    def summary_report():

        # Issue counts
        total_issues = Issue.query.count()

        open_issues = Issue.query.filter_by(
            status="Open"
        ).count()

        closed_issues = Issue.query.filter_by(
            status="Closed"
        ).count()

        # Issue priority statistics
        critical_issues = Issue.query.filter_by(
            priority="Critical"
        ).count()

        high_issues = Issue.query.filter_by(
            priority="High"
        ).count()

        medium_issues = Issue.query.filter_by(
            priority="Medium"
        ).count()

        low_issues = Issue.query.filter_by(
            priority="Low"
        ).count()

        # Vulnerability counts
        total_vulnerabilities = Vulnerability.query.count()

        critical_vulnerabilities = Vulnerability.query.filter_by(
            severity="Critical"
        ).count()

        high_vulnerabilities = Vulnerability.query.filter_by(
            severity="High"
        ).count()

        medium_vulnerabilities = Vulnerability.query.filter_by(
            severity="Medium"
        ).count()

        low_vulnerabilities = Vulnerability.query.filter_by(
            severity="Low"
        ).count()

        return jsonify({
            "total_issues": total_issues,
            "open_issues": open_issues,
            "closed_issues": closed_issues,

            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "low_issues": low_issues,

            "total_vulnerabilities": total_vulnerabilities,

            "critical_vulnerabilities": critical_vulnerabilities,
            "high_vulnerabilities": high_vulnerabilities,
            "medium_vulnerabilities": medium_vulnerabilities,
            "low_vulnerabilities": low_vulnerabilities
        }), 200
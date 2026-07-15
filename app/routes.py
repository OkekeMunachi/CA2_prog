from flask import jsonify, request
from app.database import db
from app.models import Issue, Vulnerability


def register_routes(app):

    # Home Route
    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to ACME Technologies Issue Tracker API"
        })

    # CREATE Issue
    @app.route("/issues", methods=["POST"])
    def create_issue():

        data = request.get_json()

        issue = Issue(
            title=data["title"],
            description=data["description"],
            status=data.get("status", "Open"),
            priority=data.get("priority", "Medium")
        )

        db.session.add(issue)
        db.session.commit()

        return jsonify({
            "message": "Issue created successfully",
            "issue_id": issue.id
        }), 201

    # READ ALL Issues
    @app.route("/issues", methods=["GET"])
    def get_issues():

        issues = Issue.query.all()

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
                "error": "Issue not found"
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
                "error": "Issue not found"
            }), 404

        data = request.get_json()

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
                "error": "Issue not found"
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

     # READ ALL Vulnerabilities
    @app.route("/vulnerabilities", methods=["GET"])
    def get_vulnerabilities():

        vulnerabilities = Vulnerability.query.all()

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
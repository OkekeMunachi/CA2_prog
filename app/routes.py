from flask import jsonify, request
from app.database import db
from app.models import Issue


def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to ACME Technologies Issue Tracker API"
        })

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
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
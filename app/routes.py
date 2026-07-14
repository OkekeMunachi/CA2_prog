from flask import jsonify


def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to ACME Technologies Issue Tracker API"
        })
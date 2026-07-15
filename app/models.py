from app.database import db


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    vulnerability_id = db.Column(
        db.Integer,
        db.ForeignKey("vulnerabilities.id"),
        nullable=True
    )

    def __repr__(self):
        return f"<Issue {self.title}>"

class Vulnerability(db.Model):
    __tablename__ = "vulnerabilities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    severity = db.Column(
        db.String(20),
        default="Medium"
    )

    cve_id = db.Column(
        db.String(50),
        nullable=True
    )

    issues = db.relationship(
        "Issue",
        backref="vulnerability",
        lazy=True
    )

    def __repr__(self):
        return f"<Vulnerability {self.title}>"
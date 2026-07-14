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

    def __repr__(self):
        return f"<Issue {self.title}>"
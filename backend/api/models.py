from . import db

class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    free = db.Column(db.Boolean, nullable=False)
    overview = db.Column(db.String(80))
    img = db.Column(db.String(80))
    url = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<id ={self.id}, title={self.title}, author={self.author}"
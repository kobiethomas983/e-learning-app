from .. import db

class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    free = db.Column(db.Boolean, nullable=False)
    overview = db.Column(db.Text)
    img = db.Column(db.String(512))
    url = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    categories = db.relationship(
        'Category',
        secondary='course_category_map',
        back_populates='courses'
    )

    def __repr__(self):
        return f"<id ={self.id}, title={self.title}, author={self.author}>"
    
    def to_dict(self, include_categories=False):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if include_categories:
            data['categories'] = [cat.name for cat in self.categories]
        
        return data


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    courses = db.relationship(
        'Course',
        secondary='course_category_map',
        back_populates='categories'
    )

    def to_dict(self, include_course=False):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if include_course:
            data['courses'] = [crs.to_dict() for crs in self.courses]
        
        return data


class Course_Category_Map(db.Model):
    __tablename__ = "course_category_map"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))



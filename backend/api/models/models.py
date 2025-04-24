from .. import db
from sqlalchemy import PrimaryKeyConstraint

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
            data['categories'] = [{"name": cat.name, "id": cat.id} for cat in self.categories]
        
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


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(512))

    roles = db.relationship(
        'Role',
        secondary="user_roles",
        back_populates='users'
    )

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), unique=True, nullable=False)

    users = db.relationship(
        'User',
        secondary='user_roles',
        back_populates='roles'
    )



class User_Roles(db.Model):
    __tablename__ = "user_roles"
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    __table_args__ = (
        PrimaryKeyConstraint('role_id', 'user_id'),
    )
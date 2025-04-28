import json
from api import create_app, db
from api.models.models import Course, Category, Course_Category_Map, User, Role, User_Roles
from sqlalchemy.exc import SQLAlchemyError

def seed_courses():
    try:
        with open('course.json', 'r') as file:
            json_courses = json.load(file)
            unique_categories = set()
            for jc in json_courses:
                categories = jc['categories']
                unique_categories.update(categories)
            
            try:
                categories_data = [Category(name=c.lower()) for c in unique_categories]
                db.session.add_all(categories_data)
                db.session.commit()
                print("Categories seeded succesfully")
            except SQLAlchemyError as error:
                db.session.rollback()
                print(f"Error Creating Categories: {error}")

            try:
                for jc in json_courses:
                    course = Course(
                        title=jc['title'].lower(),
                        author=jc['author'].lower(),
                        free=jc['free'],
                        overview=jc['overview'].lower(),
                        img=jc['img'],
                        url=jc['url']
                    )
                    db.session.add(course)
                db.session.commit()
                print("courses seeded successfully.")
            except SQLAlchemyError as error:
                print(f"Error Creating Courses: {error}")
                
            try:
                for jc in json_courses:
                    title = jc['title']
                    course = Course.query.filter(Course.title == title.lower()).one()

                    categories_list = [c.lower() for c in jc['categories']]
                    result = Category.query.filter(Category.name.in_(categories_list))
                    
                    for cat in result:
                        course_to_category = Course_Category_Map(
                            course_id=course.id,
                            category_id = cat.id
                        )
                        db.session.add(course_to_category)
                    db.session.commit()
                
                print("Successfully mapped category and course data")
            except SQLAlchemyError as error:
                db.session.rollback()
                print(f"Error mapping course and category data: {error}")

    except FileNotFoundError:
        print("Error: File not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")


def seed_users():
    with open('users.json', 'r') as f:
        json_users = json.load(f)

        try:
            role = [
                Role(
                    role_name = 'admin'
                ),
                Role(
                    role_name='user'
                )
            ]
            db.session.add_all(role)
            db.session.commit()

            for ju in json_users:
                user = User(
                    first_name=ju['first_name'].lower(),
                    last_name=ju['last_name'].lower(),
                    email=ju['email'].lower(),
                    password=ju['password'],
                    profile_image=ju['profile_image']
                )

                db.session.add(user)
            db.session.commit()

            for user in User.query.all():
                user_role = User_Roles(
                    role_id=2,
                    user_id=user.id
                )
                db.session.add(user_role)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            print(f"Database error: {error}")
        except FileNotFoundError:
            print(f"File not found")
        except Exception as error:
            print(f"Unknown error: {error}")




def seed_database():
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        seed_courses()
        seed_users()
    

if __name__ == '__main__':
    seed_database()
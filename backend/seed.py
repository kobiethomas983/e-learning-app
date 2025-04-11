import json
from api import create_app, db
from api.models.models import Course, Category, Course_Category_Map
from sqlalchemy.exc import SQLAlchemyError

def seed_courses():
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        try:
            with open('course_2.json', 'r') as file:
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

if __name__ == '__main__':
    seed_courses()

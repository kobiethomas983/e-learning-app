import React from 'react'
import Course from './course'


const CoursesView = ({courses, classProp}) => {
    // Handle case when courses is undefined or empty
    if (!courses || courses.length === 0) {
        return (
            <div className="container">
                <div className="alert alert-info text-center my-5">
                    No courses available. Please try again later.
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <div className={classProp}>
                {courses.map((crs, idx) => (
                    <div className="col" key={idx}>
                        <Course
                            title={crs.title}
                            author={crs.author}
                            free={crs.free}
                            img={crs.img}
                            overview={crs.overview}
                            url={crs.url}
                            categories={crs.categories}
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}
export default CoursesView;
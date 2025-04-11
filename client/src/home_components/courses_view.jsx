import React from 'react'
import Course from './course'


const CoursesView = ({courses}) => {
    return (
        <div className="container">
            <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
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
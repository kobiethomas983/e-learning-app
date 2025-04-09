import React from 'react'
import {
    Container,
    Row,
    Col
} from 'react-bootstrap'
import Course from './course'


const CoursesView = ({courses}) => {
    return (
        <Container>
            <Row>
                <Col key={200}>
                                <Course 
                                    title={courses[0].title}
                                    author={courses[0].author}
                                    free={courses[0].free}
                                    img={courses[0].img}
                                    overview={courses[0].overview}
                                    url={courses[0].url}
                                />
                    </Col>
                    <Col key={200}>
                                <Course 
                                    title={courses[1].title}
                                    author={courses[1].author}
                                    free={courses[1].free}
                                    img={courses[1].img}
                                    overview={courses[1].overview}
                                    url={courses[1].url}
                                />
                    </Col>
            </Row>
            <Row>
                {courses.map((crs, idx) => (
                        // gives different cols in row base on screen size
                        <Col key={idx} xs={12} sm={6} md={4} lg={3}>
                            <Course 
                                title={crs.title}
                                author={crs.author}
                                free={crs.free}
                                img={crs.img}
                                overview={crs.overview}
                                url={crs.url}
                            />
                        </Col>
                ))}
            </Row>
        </Container>
    )
}
export default CoursesView;
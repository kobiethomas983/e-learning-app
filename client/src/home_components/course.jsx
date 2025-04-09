import React from 'react'
// import { useNavigate } from 'react-router-dom'
import {
    Card,
    ListGroup,
    Button
} from 'react-bootstrap'

const Course = ({title, author, free, img, overview, url}) => {
    // const navigate = useNavigate();

    const handleClick = () => {
        console.log("Opening URL:", url)
        window.open(url, '_blank')
    }

    return(
        <Card className="h-100">
            <div style={{ height: '180px', overflow: 'hidden' }}>
                <Card.Img variant="top" src={img ? img : "holder.js/100px180?text=Image cap"} />
            </div>
            <Card.Body>
                <Card.Title>{title}</Card.Title>
                <Card.Text>{overview}</Card.Text>
            </Card.Body>
            <ListGroup className="list-group-flush">
                <ListGroup.Item>Author: {author}</ListGroup.Item>
                {free == true && (
                    <ListGroup.Item>Free</ListGroup.Item>
                )}
            </ListGroup>
            <Card.Body>
                <Button onClick={handleClick} variant='primary'>Check Site</Button>
            </Card.Body>
        </Card>
    )
}

export default Course;
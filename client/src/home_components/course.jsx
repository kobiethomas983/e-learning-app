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

    const formatBriefOverview = (overview) => {
        if (overview.length > 100) {
            return overview.slice(0, 100) + '...'
        }
        return overview
    }

    return(
        <Card className="h-100">
            <div style={{ height: '180px', overflow: 'hidden' }}>
                <Card.Img variant="top" src={img ? img : "holder.js/100px180?text=Image cap"} />
            </div>
            <Card.Body>
                <Card.Title>{title}</Card.Title>
                <Card.Text>{formatBriefOverview(overview)}</Card.Text>
            </Card.Body>
            <ListGroup className="list-group-flush">
                <ListGroup.Item><strong>Author:</strong> {author}</ListGroup.Item>
                {free == true && (
                    <ListGroup.Item><strong>Free</strong></ListGroup.Item>
                )}
            </ListGroup>
            <Card.Body>
                <Button onClick={handleClick} variant='primary'>Check Site</Button>
            </Card.Body>
        </Card>
    )
}

export default Course;
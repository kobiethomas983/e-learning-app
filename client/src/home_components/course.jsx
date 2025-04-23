import React from 'react'
import {
    Card,
    ListGroup,
    Button
} from 'react-bootstrap'

import "./styles.css"


const Course = ({title, author, free, img, overview, url, categories, onCategoryFetch, onAuthorFetch, singleCardView}) => {

    const handleClickOnSite = () => {
        console.log("Opening URL:", url)
        window.open(url, '_blank')
    }

    const handleClickOnCategory = (category_id) => {
        onCategoryFetch(category_id);
    }

    const handleClickOnAuthor = (author) => {
        onAuthorFetch(author);
    }

    const formatBriefOverview = (overview) => {
        if (overview.length > 100) {
            return overview.slice(0, 100) + '...'
        }
        return overview
    }

    const capitalize = (str) => {
        if (!str) return '';
        return str[0].toUpperCase() + str.slice(1).toLowerCase();
    }

    // Apply a max-width when in single card view to prevent stretching
    const cardStyle = singleCardView ? { maxWidth: '22rem' } : {};

    return(
        <Card className={`h-100 ${singleCardView ? 'single-card' : ''}`} style={cardStyle}>
            <div style={{ height: '180px', overflow: 'hidden' }}>
                <Card.Img variant="top" src={img ? img : "holder.js/100px180?text=Image cap"} />
            </div>
            <Card.Body>
                <Card.Title>{title}</Card.Title>
                <Card.Text>{formatBriefOverview(overview)}</Card.Text>
            </Card.Body>
            <ListGroup className="list-group-flush">
                <ListGroup.Item>
                    <strong>Author:</strong> 
                    <a 
                        className='category-link'
                        onClick={() => handleClickOnAuthor(author)}
                    >
                        {author}
                    </a>
                </ListGroup.Item>
                {free == true
                 ? <ListGroup.Item><strong>Free-Course</strong></ListGroup.Item>
                 : <ListGroup.Item><strong>Paid-Course</strong></ListGroup.Item>
                }
                <ListGroup.Item>
                    <p>
                        {categories?.map((category, index) => {
                        return <a
                                    key={index}
                                    className='category-link'
                                    onClick={() =>handleClickOnCategory(category.id)}
                                >
                                    {capitalize(category?.name)}
                                </a>
                })}
                 </p>
                </ListGroup.Item>
            </ListGroup>
            <Card.Body>
                <Button onClick={handleClickOnSite} variant='primary'>Check Site</Button>
            </Card.Body>
        </Card>
    )
}

export default Course;
import React, {useState, useEffect} from "react";
import CoursesView from "./courses_view";
import { Pagination } from "react-bootstrap";

import axios from "axios";
const base_url = "http://localhost:5000";

export const Dashboard = () => {
    const [courses, setCourses] = useState([]);
    const [pageNumber, setPageNumber] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [courseCount, setCourseCount] = useState(0)
    const [loading, setLoading] = useState(true);
    const pageSize = 6; // Number of courses per page

    useEffect(() => {
        const fetchCourses = async () => {
            setLoading(true);
            try {
                const response = await axios.get(`${base_url}/courses?page=${pageNumber}&page_size=${pageSize}`);
                setCourses(response?.data?.courses);
                setTotalPages(response?.data?.total_pages || 1);
                setCourseCount(response?.data?.total_course)
            } catch (error) {
                alert(`Error retrieving courses: ${error}`);
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, [pageNumber, pageSize]);

    // Handle page change
    const handlePageChange = (newPage) => {
        setPageNumber(newPage);
        window.scrollTo(0, 0);
    };

    // Generate pagination items
    const renderPaginationItems = () => {
        const items = [];

        // Previous button
        items.push(
            <Pagination.Prev
                key="prev"
                onClick={() => handlePageChange(pageNumber - 1)}
                disabled={pageNumber === 1}
            />
        );

        // Page numbers
        for (let number = 1; number <= totalPages; number++) {
            items.push(
                <Pagination.Item
                    key={number}
                    active={number === pageNumber}
                    onClick={() => handlePageChange(number)}
                >
                    {number}
                </Pagination.Item>
            );
        }

        // Next button
        items.push(
            <Pagination.Next
                key="next"
                onClick={() => handlePageChange(pageNumber + 1)}
                disabled={pageNumber === totalPages}
            />
        );

        return items;
    };

    return(
        <div className="container my-4">
            {loading ? (
                <div className="text-center my-5">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                    <p className="mt-2">Loading courses...</p>
                </div>
            ) : (
                <>
                    <CoursesView courses={courses}/>

                    {/* Pagination controls */}
                    {totalPages > 1 && (
                        <div className="d-flex justify-content-center mt-4">
                            <Pagination>{renderPaginationItems()}</Pagination>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
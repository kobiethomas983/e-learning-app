import React, {useState, useEffect} from "react";
import CoursesView from "../home_components/courses_view";
import { Pagination } from "react-bootstrap";

import axios from "axios";
import { BASE_URL, DEFAULT_PAGE_SIZE } from "../utils";

export const CategoryCourseView = ({id}) => {
    const [pageNumber, setPageNumber] = useState(1);
    const [courses, setCourses] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchCoursesByCategory = () => {
            try {
                const response = axios.get(`${BASE_URL}/courses/categories/${id}?page=${pageNumber}&page_size=${DEFAULT_PAGE_SIZE}`);
                setCourses(response?.data?.courses);
                setTotalPages(response?.data?.total_pages || 1);
            } catch(error) {
                alert(`Error retrieving courses: ${error}`);
            } finally {
                setLoading(false);
            }
        };
        fetchCoursesByCategory();
    }, [courses]);


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

    return (
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
                    <CoursesView courses={courses} classProp="row row-cols-1"/>

                    {/* Pagination controls */}
                    {totalPages > 1 && (
                        <div className="d-flex justify-content-center mt-4">
                            <Pagination>{renderPaginationItems()}</Pagination>
                        </div>
                    )}
                </>
            )}
      </div>
    )


}
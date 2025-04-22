import React, {useState, useEffect} from "react";
import CoursesView from "./courses_view";
import { Pagination } from "react-bootstrap";

import axios from "axios";
import { BASE_URL, DEFAULT_PAGE_SIZE } from "../utils";
import { ShowIf } from "../global";

export const Dashboard = () => {
    const [courses, setCourses] = useState([]);
    const [pageNumber, setPageNumber] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [courseCount, setCourseCount] = useState(0)
    const [loading, setLoading] = useState(true);
    const [style, setStyle] = useState("row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4")
    const [singleCardView, setSingleCardView] = useState(false)
    // const [mainViewVisible, setMainViewVisible] = useState(false);

    useEffect(() => {
        const fetchCourses = async () => {
            setLoading(true);
            try {
                const response = await axios.get(`${BASE_URL}/courses?page=${pageNumber}&page_size=${DEFAULT_PAGE_SIZE}`);
                setCourses(response?.data?.courses);
                setTotalPages(response?.data?.total_pages || 1);
                setCourseCount(response?.data?.total_course);
                // Reset to multi-card view
                setStyle("row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4");
                setSingleCardView(false);
            } catch (error) {
                alert(`Error retrieving courses: ${error}`);
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, [pageNumber]);

    const fetchCoursesByCategory = async (id) => {
        setLoading(true);
        try {
            const response = await axios.get(`${BASE_URL}/courses/categories/${id}?page=${pageNumber}&page_size=${DEFAULT_PAGE_SIZE}`);
            setCourses(response?.data?.courses);
            setTotalPages(response?.data?.total_pages || 1);
            setStyle("row row-cols-1");
            setSingleCardView(true);
        } catch(error) {
            alert(`Error retrieving courses: ${error}`);
        } finally {
            setLoading(false);
        }
    }

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
            <ShowIf condition={loading}>
            <div className="text-center my-5">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                    <p className="mt-2">Loading courses...</p>
                </div>
            </ShowIf>
            <ShowIf condition={!loading}>
                <>
                    <CoursesView
                        courses={courses}
                        classProp={style}
                        onCategoryFetch={fetchCoursesByCategory}
                        singleCardView={singleCardView}
                    />
                    {/* Pagination controls */}
                    {totalPages > 1 && (
                        <div className="d-flex justify-content-center mt-4">
                            <Pagination>{renderPaginationItems()}</Pagination>
                        </div>
                    )}
                </>
            </ShowIf>
        </div>
    );
}
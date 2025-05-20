import React, {useState, useEffect, useRef} from "react";
import CoursesView from "./courses_view";
import { Pagination, Form, FormControl, Button, InputGroup } from "react-bootstrap";

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
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const searchTimeout = useRef(null);
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

    // Hide dropdown when clicking outside
    useEffect(() => {
        const handleClick = (e) => {
            if (!e.target.closest(".search-dropdown-container")) {
                setShowDropdown(false);
            }
        };
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);

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

    const fetchCoursesByAuthor = async(author) => {
        setLoading(true);
        try {
            const response = await axios.get(
                `${BASE_URL}/courses?pages=${pageNumber}&page_size=${DEFAULT_PAGE_SIZE}&author_filter=${author}`
            )
            setCourses(response?.data?.courses);
            setTotalPages(response?.data?.total_pages);
            setStyle("row row-cols-1");
            setSingleCardView(true);
        } catch (error) {
            alert(`Error retrieving courses by author: ${error}`);
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

    const handleResultClick = (courses) => {
        setShowDropdown(false);
        console.log("Opening URL:", courses.url)
        window.open(courses.url, '_blank');
    }

    const handleSearchChange = (e) => {
        const value = e.target.value;
        setSearchQuery(value);

        if (value.trim()) {
            if (searchTimeout.current) clearTimeout(searchTimeout.current);

            searchTimeout.current = setTimeout(async () => {
                try {
                    const response = await axios.get(
                        `${BASE_URL}/courses/search?q=${encodeURIComponent(value)}`
                    );
                    const filteredCourses = response.data?.filter((course, index) => index < 6);

                    setSearchResults(filteredCourses);
                    setShowDropdown(true);
                } catch (error) {
                    console.error("Error fetching search results:", error);
                    setSearchResults([]);
                    setShowDropdown(false);
                }
            }, 300); // debounce delay
        } else {
            setSearchResults([]);
            setShowDropdown(false);
        }
    };



    return(
        <div className="container my-4">
             <div className="search-dropdown-container" style={{position: "relative"}}>
                <Form className="mb-4">
                    <InputGroup className="mb-3">
                        <FormControl
                            type="text"
                            placeholder="Search for courses..."
                            aria-label="Search for courses"
                            aria-describedby="search-button"
                            value={searchQuery}
                            onChange={handleSearchChange}
                            onFocus={() => searchResults?.length > 0 && setShowDropdown(true)}
                        />
                        <Button variant="outline-secondary" id="``search-button">
                            Search
                        </Button>
                    </InputGroup>
                    {showDropdown && searchResults?.length > 0 && (
                        <div
                            style={{
                                position: "absolute",
                                top: "100%",
                                left: 0,
                                right: 0,
                                zIndex: 1000,
                                background: "#fff",
                                border: "1px solid #ccc",
                                borderTop: "none",
                                maxHeight: "250px",
                                overflowY: "auto"
                            }}
                        >
                            {searchResults.map(course => (
                                <div
                                    key={course.id}
                                    style={{ padding: "10px", cursor: "pointer", borderBottom: "1px solid #eee" }}
                                    onClick={() => handleResultClick(course)}
                                >
                                    {course.title}
                                </div>
                            ))}
                        </div>
                    )}
                </Form>
             </div>
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
                        onAuthorFetch={fetchCoursesByAuthor}
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
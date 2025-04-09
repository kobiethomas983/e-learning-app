import React from "react";
import course_data from "./mock_data";
import CoursesView from "./courses_view";

export const Dashboard = () => {
    return(
        <CoursesView courses={course_data}/>
    )
}
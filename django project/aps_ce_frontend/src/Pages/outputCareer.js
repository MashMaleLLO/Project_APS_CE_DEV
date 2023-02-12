import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import _ from "lodash";

const baseURL = "http://localhost:8000/students";

const OutputCareer = () => {
  const [posts, setPosts] = useState([]);
  const [startYear, setStartYear] = useState("");

  useEffect(() => {
    axios.get(baseURL).then((response) => {
      setPosts(response.data);
    });
  }, [startYear]);

  if (!posts) return null;

  const careerCount = _.countBy(posts, "career");
  const filteredPosts = posts.filter(
    (post) => post.start_year === startYear || startYear === ""
  );

  const filteredCareers = Object.entries(
    careerCount
  ).filter(([career, count]) =>
    filteredPosts.some(
      (post) =>
        post.career === career &&
        post.career !== "Zero" &&
        post.career !== "ไม่มีงาน"
    )
  );

  return (
    <>
      <h1>Careers</h1>
      <select onChange={(e) => setStartYear(e.target.value)} value={startYear}>
        <option value="">All</option>
        <option value="2560">2560</option>
        <option value="2561">2561</option>
        <option value="2562">2562</option>
        <option value="2563">2563</option>
      </select>
      <ul>
        {filteredCareers.map(([career, count]) => (
          <li key={career}>
            {career}: {count}
          </li>
        ))}
      </ul>
    </>
  );
};

export default OutputCareer;

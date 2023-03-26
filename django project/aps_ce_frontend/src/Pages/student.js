import React, { useState } from "react";
import axios from "axios";

function Student() {
  const [id, setId] = useState("");
  const [career, setCareer] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    axios
      .put(
        `${process.env.REACT_APP_BACKEND_URL}/update_student_career_by_one`,
        {
          id: id,
          career: career,
        }
      );
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Student ID:
        <input type="text" value={id} onChange={(e) => setId(e.target.value)} />
      </label>
      <label>
        Career:
        <input
          type="text"
          value={career}
          onChange={(e) => setCareer(e.target.value)}
        />
      </label>
      <button type="submit">Update Career</button>
    </form>
  );
}

export default Student;

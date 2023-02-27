import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const RecommendedSubjectsList = ({ subjects }) => {
  const navigate = useNavigate();
  const [selectedSubject, setSelectedSubject] = useState(null);

  const handleClick = (subject) => {
    setSelectedSubject(subject);
  };

  const handleCloseModal = () => {
    setSelectedSubject(null);
  };

  return (
    <div>
      <h1>Recommended Subjects:</h1>
      <ul>
        {subjects.map((subject) => (
          <li key={subject.subject_id}>
            <span onClick={() => handleClick(subject)}>
              {subject.subject_name_eng}
            </span>
          </li>
        ))}
      </ul>
      {selectedSubject && (
        <div>
          <p>Subject ID: {selectedSubject.subject_id}</p>
          <p>Abstract: {selectedSubject.abstract}</p>
          <button onClick={handleCloseModal}>Close</button>
        </div>
      )}
      <button onClick={() => navigate(`recommendSubject`)}>Back to RecommendSubject</button>
    </div>
  );
};

export default RecommendedSubjectsList;

import React, { useState } from "react";
import RecommendSubject from "./recommendSubject.js";

const RecommendedSubjectsList = ({ subjects }) => {
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [back, setBack] = useState(false);

  const handleClick = (subject) => setSelectedSubject(subject);
  const handleCloseModal = () => setSelectedSubject(null);

  return (
    <>
      {back ? (
        <RecommendSubject />
      ) : (
        <div>
          <h1>Recommended Subjects:</h1>
          <form onSubmit={() => setBack(true)}>
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
            <button type="submit">Back to RecommendSubject</button>
          </form>
        </div>
      )}
    </>
  );
};

export default RecommendedSubjectsList;
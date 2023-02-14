import { useState, useEffect } from 'react';
import React from 'react';
import axios from 'axios';

function OutputCareer() {
  const [careerData, setCareerData] = useState({});

  useEffect(() => {
    axios.get('http://localhost:8000/getCareerResult')
      .then(response => {
        setCareerData(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  console.log(careerData);

  return (
    <div>
      <h1>Career Result</h1>
      <ul>
        {Object.keys(careerData).map((career, index) => (
          <li key={index}>
            {career}: {careerData[career].Num_of_student}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default OutputCareer;
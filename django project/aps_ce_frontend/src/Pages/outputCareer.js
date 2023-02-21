import { useState, useEffect } from "react";
import React from "react";
import axios from "axios";

function OutputCareer() {
  const [careerData, setCareerData] = useState({});
  const [outputType, setOutputType] = useState("staticResult");
  const [selectedYear, setSelectedYear] = useState("");

  useEffect(() => {
    if (outputType == "staticResult") {
      axios
        .get("http://localhost:8000/getCareerResult/")
        .then((response) => {
          setCareerData(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    } else if (outputType == "staticPredictResult") {
      axios
        .get("http://localhost:8000/getCareerResult/")
        .then((response) => {
          setCareerData(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [outputType]);

  const handleYearChange = (event) => {
    setSelectedYear(event.target.value);
  };

  const filteredCareerData = Object.entries(careerData).reduce(
    (acc, [career, data]) => {
      if (selectedYear === "" || data.Year === selectedYear) {
        acc[career] = data;
      }
      return acc;
    },
    {}
  );

  const handleButtonClick = (type) => {
    setOutputType(type);
    setSelectedYear("");
  };

  return (
    <>
      <div>
        <button onClick={() => handleButtonClick("staticResult")}>
          Static Result
        </button>
        <br></br>
        <button onClick={() => handleButtonClick("staticPredictResult")}>
          Static Predict Result
        </button>
      </div>
      <br></br>
      <br></br>
      {outputType == "staticResult" ? (
        <div>
          <h1>Career Result</h1>
          <div>
            <label htmlFor="year-select">Select a year:</label>
            <select
              id="year-select"
              value={selectedYear}
              onChange={handleYearChange}
            >
              <option value="">All years</option>
              <option value="2561">2561</option>
              <option value="2560">2560</option>
            </select>
          </div>
          <ul>
            {Object.keys(filteredCareerData).map((career, index) => (
              <li key={index}>
                {career}: {filteredCareerData[career].Num_of_student}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div></div>
      )}
    </>
  );
}

export default OutputCareer;

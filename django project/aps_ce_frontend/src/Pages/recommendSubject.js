import { useState, useEffect } from "react";
import React from "react";
import axios from "axios";

const RecommendSubject = () => {
  const [year, setYear] = useState("2564");
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjects, setSelectedSubjects] = useState([]);

  const handleYearChange = (e) => {
    setYear(e.target.value);
  };

  const handleCheckboxChange = (e) => {
    const value = e.target.value;
    const isChecked = e.target.checked;
    if (isChecked) {
      setSelectedSubjects([...selectedSubjects, value]);
    } else {
      setSelectedSubjects(selectedSubjects.filter((s) => s !== value));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await axios.post("http://localhost:8000/recommendSubject", {
      key: selectedSubjects,
      year: year,
    });
    setSubjects(result.data);
  };

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.post("http://localhost:8000/keysubject", {
        year: year,
      });
      setSubjects(result.data);
    };
    fetchData();
  }, [year]);

  return (
    <>
      <h1>แนะนำวิชาเลือกภาค</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="select-faculty">คณะ</label>
        <select
          id="select-faculty"
          className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
        >
          <option value="computer">วิศวกรรมคอมพิวเตอร์</option>
          <option value="computerNext">วิศวกรรมคอมพิวเตอร์(ต่อเนื่อง)</option>
        </select>
        <label htmlFor="select-year">หลักสูตร</label>
        <select
          id="select-year"
          className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
          onChange={handleYearChange}
          value={year}
        >
          <option value="2560">2560</option>
          <option value="2564">2564</option>
        </select>
        <div>
          {subjects.map((subject) => (
            <div key={subject}>
              <label>
                <input
                  type="checkbox"
                  value={subject}
                  checked={selectedSubjects.includes(subject)}
                  onChange={handleCheckboxChange}
                />
                {subject}
              </label>
            </div>
          ))}
        </div>
        <button type="submit">แนะนำวิชาเลือกภาค</button>
      </form>
    </>
  );
};

export default RecommendSubject;
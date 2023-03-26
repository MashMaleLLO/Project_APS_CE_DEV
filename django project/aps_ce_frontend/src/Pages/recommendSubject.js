import { useState, useEffect } from "react";
import React from "react";
import axios from "axios";
import RecommendedSubjectsList from "./recommendedSubjectsList.js";

const RecommendSubject = () => {
  const [year, setYear] = useState("2564");
  const [keys, setKeys] = useState([]);
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

  const [showSubjects, setShowSubjects] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/recommendSubject`, {
      key: selectedSubjects,
      year: year,
    });
    setSubjects(result.data);
    console.log("โชว์ดาต้าrecommendSubject", result.data);
    setShowSubjects(true); // show the subjects list
  };

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/keysubject`, {
        year: year,
      });
      setKeys(result.data);
      console.log("โชว์ดาต้าkeysubject", result.data);
    };
    fetchData();
  }, [year]);

  return (
    <>
      {showSubjects ? (
        <RecommendedSubjectsList subjects={subjects} year={year}/>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col h-full pb-20 2xl:min-h-screen">
            <div className="container mx-auto py-8 px-8 md:px-32">
              <h1 className="py-12 text-xl md:text-2xl font-bold">
                เเนะนำวิชาเลือกภาค
              </h1>
              <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-4 py-8 space-y-6 w-full h-full">
                <div className="flex flex-wrap gap-8">
                  <div className="space-y-2 text-sm md:text-base w-full md:w-[25%]">
                    <label htmlFor="select-faculty">คณะ</label>
                    <select
                      id="select-faculty"
                      className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                    >
                      <option value="computer">วิศวกรรมคอมพิวเตอร์</option>
                      <option value="computerNext">
                        วิศวกรรมคอมพิวเตอร์(ต่อเนื่อง)
                      </option>
                    </select>
                  </div>

                  <div className="space-y-2 text-sm md:text-base w-full md:w-[25%]">
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
                  </div>
                </div>

                <h1 className="text-sm md:text-base">เลือกความสนใจ</h1>
                <div className="flex flex-wrap gap-4">
                  {keys.map((subject) => (
                    <div className="flex items-center gap-2">
                      <div className="relative flex items-center">
                        <input
                          id="checkbox"
                          type="checkbox"
                          className="absolute peer  w-full h-full opacity-0 accent-blue-300 focus:accent-blue-500 rounded-full"
                          value={subject}
                          checked={selectedSubjects.includes(subject)}
                          onChange={handleCheckboxChange}
                        />
                        <label
                          for="checkbox"
                          className="p-8 text-black border border-grey-300 text-sm md:text-base px-4 py-2 rounded-lg select-none peer peer-checked:bg-[#FF9D2E] peer-checked:border-[#FF9D2E] peer-checked:text-white cursor-pointer"
                        >
                          {subject}
                        </label>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex justify-center py-4">
                  <button
                    type="submit"
                    className="w-[160px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                  >
                    แนะนำวิชาเลือกภาค
                  </button>
                </div>
              </div>
            </div>
          </div>
        </form>
      )}
    </>
  );
};

export default RecommendSubject;

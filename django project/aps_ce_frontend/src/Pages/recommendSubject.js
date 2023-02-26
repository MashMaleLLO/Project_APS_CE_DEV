import { useState, useEffect } from "react";
import React from "react";
import axios from "axios";

const RecommendSubject = () => {
  const [year, setYear] = useState("2564"); // default value for year is 2564

  const handleYearChange = (e) => {
    setYear(e.target.value); // update the year state when the user selects a different year
  };

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get("http://localhost:8000/getkeysubject", {
        year: year, // send the selected year in the request body as a JSON object
      });
      console.log(result.data); // log the response from the API
      // TODO: update your UI based on the response data
    };
    fetchData();
  }, [year]); // re-run the effect when the year state changes

  return (
    <div className="flex flex-col min-h-screen justify-between">
      <div className="container mx-auto py-8 px-4">
        <h1 className="py-12 text-xl md:text-2xl font-bold">
          แนะนำวิชาเลือกภาค
        </h1>
        <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-8 py-8 space-y-6 w-full h-[500px]">
          <div className="flex flex-wrap items-end gap-8">
            <div className="space-y-2 text-base md:text-lg w-full md:w-1/4">
              {/* เเถวที่ 1 : Dropdown*/}
              <label htmlFor="select-option">คณะ</label>
              <select
                id="select-option"
                className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
              >
                <option value="computer">วิศวกรรมคอมพิวเตอร์</option>
                <option value="computerNext">วิศวกรรมคอมพิวเตอร์(ต่อเนื่อง)</option>
              </select>
            </div>
            <div className="space-y-2 text-base md:text-lg w-full md:w-1/4">
              <label htmlFor="select-option">หลักสูตร</label>
              <select
                id="select-option"
                className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                onChange={handleYearChange} // call handleYearChange when the user selects a different year
                value={year} // set the selected year as the value of the dropdown
              >
                <option value="2560">2560</option>
                <option value="2564">2564</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendSubject;
import React, { useState } from "react";
import axios from "axios";

function Student() {
  const [id, setId] = useState("");
  const [career, setCareer] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.put(
      `${process.env.REACT_APP_BACKEND_URL}/update_student_career_by_one`,
      {
        id: id,
        career: career,
      }
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="flex flex-col h-[calc(100vh-64px)] 2xl:h-[calc(100vh-128px)]">
        <div className="container mx-auto py-8 px-8 md:px-32">
          <h1 className="py-12 text-xl md:text-2xl font-bold">
            นักศึกษา
          </h1>
          <div className="container mx-auto flex flex-col md:flex-row justify-start items-start px-4 py-8 rounded-lg drop-shadow-md bg-white w-full h-[350px]">
            <div className="flex flex-wrap items-end gap-6">
              <div className="space-y-2 text-sm md:text-base">
                <label>รหัสนักศึกษา</label>
                <input
                  type="text"
                  value={id}
                  onChange={(e) => setId(e.target.value)}
                  className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                />
              </div>
              <div className="space-y-2 text-sm md:text-base">
                <label>อาชีพ</label>
                <input
                  type="text"
                  value={career}
                  onChange={(e) => setCareer(e.target.value)}
                  className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                />
              </div>

              <div className="space-y-2">
                <button
                  type="submit"
                  className="w-[150px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                >
                  อัพโหลดอาชีพ
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  );
}

export default Student;

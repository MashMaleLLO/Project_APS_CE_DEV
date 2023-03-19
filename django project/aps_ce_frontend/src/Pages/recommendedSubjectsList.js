import React, { useState } from "react";
import RecommendSubject from "./recommendSubject.js";
import RecommendModal from "../Component/recommendModal.js";

const RecommendedSubjectsList = ({ year , subjects}) => {
  const [back, setBack] = useState(false);
  const [selectedSubject, setSelectedSubject] = useState([]);

  const handleClick = (subject) => setSelectedSubject(subject);

  console.log("subjectlists", subjects);
  console.log("kuay", selectedSubject);
  console.log("handleClick", handleClick);
  console.log("year : ", year);

  return (
    <>
      {back ? (
        <RecommendSubject />
      ) : (
        <form onSubmit={() => setBack(true)}>
          <div className="flex flex-col mx-auto py-8 px-8 md:mb-20 md:px-32 xl:mb-36">
            <h1 className="py-12 text-xl md:text-2xl font-bold text-center">
              เเนะนำวิชาเลือกภาค
            </h1>
            {/* <h1>Recommended Subjects:</h1> */}
            <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-8 py-8 space-y-6 w-full ">
              <h1 className="text-base md:text-lg font-medium">
                วิชาเลือกภาคที่แนะนำ คณะวิศวกรรมคอมพิวเตอร์ หลักสูตร {year}
              </h1>

              <div>
                <ul className="space-y-2">
                  {subjects.map((subject, index) => (
                    <li
                      key={subject.subject_id}
                      onClick={() => handleClick(subject)}
                      className={`flex items-center justify-between text-sm md:text-base py-2 border-b-[1.5px] border-[#A7A7A7] ${
                        index === subjects.length - 1 && "border-b-0 border-white"
                      }`}
                    >
                      <div className="text-sm md:text-base">
                        {subject.subject_name_eng}
                      </div>
                      <RecommendModal subjects={selectedSubject} />
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex justify-center py-4">
                <button
                  type="submit"
                  className="w-[80px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                >
                  กลับ
                </button>
              </div>
            </div>
          </div>
        </form>
      )}
    </>
  );
};

export default RecommendedSubjectsList;

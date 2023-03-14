import React, { useState, useEffect } from "react";
// import PredictUpload from "./components/PredictUpload";
// import StaticUpload from "./components/StaticUpload";

const Upload = () => {
  //เลือกหัวข้อ
  const [selectedButton, setselectedButton] = useState("button1");

  const handleButtonClick = (button) => {
    setselectedButton(button);
  };

  return (
    <div className="w-full py-12 min-h-screen">
      <div className="flex flex-col items-center justify-center">
        <div className="flex items-center">
          <button
            className={`${
              selectedButton === "button1" ? "text-black" : "text-[#A7A7A7]"
            } text-xl md:text-2xl font-bold cursor-pointer py-4 px-4`}
            onClick={() => handleButtonClick("button1")}
          >
            ข้อมูลนักศึกษา
          </button>
          <span className="text-xl md:text-2xl">|</span>
          <button
            className={`${
              selectedButton === "button2" ? "text-black" : "text-[#A7A7A7]"
            } text-xl md:text-2xl font-bold cursor-pointer py-4 px-4`}
            onClick={() => handleButtonClick("button2")}
          >
            หลักสูตรวิชา
          </button>
        </div>

        {selectedButton === "button1" ? (
          <div className="flex flex-col">
            {/* <StaticUpload /> */}
          </div>
        ) : (
          <div className="flex flex-col">
            {/* <PredictUpload /> */}
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload;

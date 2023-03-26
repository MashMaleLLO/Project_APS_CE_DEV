import React, { useState } from "react";
import axios from "axios";
import ResultPredict from "./resultPredict.js";

const PredictStudent = () => {
  let formData = new FormData();
  const [csvFile, setCsvFile] = useState();
  const [year, setYear] = useState("2560");
  const [curriculum, setCurriculum] = useState("วิศวกรรมคอมพิวเตอร์");
  const [predicts, setPredicts] = useState([]);
  const [showPredicts, setShowPredicts] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleYearChange = (e) => {
    setYear(e.target.value);
  };

  const handleCurriculum = (e) => {
    setCurriculum(e.target.value);
  };

  if (csvFile) {
    formData.append("path_to_csv", csvFile);
  }

  const handleChange = (e) => {
    if (e.currentTarget.files) setCsvFile(e.currentTarget.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // console.log(e.target.model.value);
    console.log(formData['path_to_csv']);
    async function fetchData() {
      setIsLoading(true);
      let res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/reqPredict`, formData);
      console.log(res.data);
      setPredicts(res.data);
      setShowPredicts(true);
      setIsLoading(false);
    }
    fetchData();
  };

  const getDownloadFile = (e) => {
    e.preventDefault();
    async function getfile() {
      let res = await axios
        .post(`${process.env.REACT_APP_BACKEND_URL}/reqAna`, {
          curriculum: curriculum,
          year: year,
          responseType: "blob",
        })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "2560fileformat.csv"); //or any other extension
          document.body.appendChild(link);
          link.click();
        });
    }
    console.log(curriculum);
    getfile();
  };

  return (
    <>
      {showPredicts ? (
        <ResultPredict predicts={predicts} year={year}/>
      ) : (
        <div className="flex flex-col h-[calc(100vh-64px)] 2xl:h-[calc(100vh-128px)] justify-between">
          <div className="container mx-auto py-8 px-8 md:px-32">
            <h1 className="py-12 text-xl md:text-2xl font-bold">
              พยากรณ์นักศึกษา
            </h1>
            <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-4 py-8 space-y-6 w-full h-[420px]">
              <form onSubmit={getDownloadFile}>
                <div className="flex items-end flex-wrap gap-8">
                  <div className="space-y-2 text-sm md:text-base w-full md:w-[25%]">
                    {/* เเถวที่ 1 : Dropdown*/}
                    <label htmlFor="select-option">หลักสูตร</label>
                    <select
                      id="select-year"
                      className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                      onChange={handleCurriculum}
                      value={curriculum}
                    >
                      <option value="วิศวกรรมคอมพิวเตอร์">
                        วิศวกรรมคอมพิวเตอร์
                      </option>
                      <option value="วิศวกรรมคอมพิวเตอร์(ต่อเนื่อง)">
                        วิศวกรรมคอมพิวเตอร์(ต่อเนื่อง)
                      </option>
                    </select>
                  </div>
                  <div className="space-y-2 text-sm md:text-base w-full md:w-[25%]">
                    <label htmlFor="select-option">ปี</label>
                    <select
                      id="select-year"
                      className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                      onChange={handleYearChange}
                      value={year}
                    >
                      <option value="2562">2562</option>
                      <option value="2563">2563</option>
                      <option value="2564">2564</option>
                    </select>
                  </div>
                  <div className="w-full md:w-[25%]">
                    <button
                      type="download"
                      className="text-white text-sm md:text-base px-4 py-2 rounded-lg bg-[#FF9D2E] hover:bg-[#F28204]"
                    >
                      ดาวน์โหลดไฟล์แบบฟอร์มสำหรับการวิเคราะห์
                    </button>
                  </div>
                </div>
              </form>

              {/* เเถวที่ 2 : uplaod file + พยากรณ์*/}
              <form onSubmit={handleSubmit}>
                <div className="flex flex-wrap gap-8">
                  <div className="w-full md:w-1/4 ">
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleChange}
                      className="w-full px-4 py-1 text-gray-500 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none
              file:bg-[#FF9D2E] file:rounded-lg file:border-none file:px-2.5 file:py-1.5 file:text-white file:cursor-pointer file:mr-4"
                    />
                  </div>
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <button
                        type="button"
                        className="inline-flex items-center px-4 py-2 text-sm font-semibold leading-6 text-white transition duration-150 ease-in-out bg-indigo-500 rounded-md shadow cursor-not-allowed hover:bg-indigo-400"
                        disabled=""
                      >
                        <svg
                          className="w-5 h-5 mr-3 -ml-1 text-white animate-spin"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Loading...
                      </button>
                    </div>
                  ) : (
                    <div>
                      <button
                        type="submit"
                        className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                      >
                        พยากรณ์
                      </button>
                    </div>
                  )}
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
      ;
    </>
  );
};

export default PredictStudent;

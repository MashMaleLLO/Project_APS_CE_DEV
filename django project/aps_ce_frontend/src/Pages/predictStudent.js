import React, { useState } from "react";
import axios from "axios";
import ModelList from "./modelList";
import YearList from "./listPossibleYear";

const PredictStudent = () => {
  let formData = new FormData();
  const [csvFile, setCsvFile] = useState();
  if (csvFile) {
    formData.append("path_to_csv", csvFile);
  }

  const handleChange = (e) => {
    if (e.currentTarget.files) setCsvFile(e.currentTarget.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(e.target.model.value);
    async function fetchData() {
      let res = await axios.post("http://localhost:8000/reqPredict", formData);
      console.log(res.data);
    }

    fetchData();
  };

  const getDownloadFile = (e) => {
    e.preventDefault();
    async function getfile() {
      let res = await axios({
        url:
          "http://localhost:8000/reqAna/" +
          e.target.curri.value +
          "/" +
          e.target.year.value, //your url
        method: "GET",
        responseType: "blob", // important
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "2560fileformat.csv"); //or any other extension
        document.body.appendChild(link);
        link.click();
      });
    }
    getfile();
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="py-4 text-xl md:text-2xl font-bold">พยากรณ์นักศึกษา</h1>
      <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-8 py-8 space-y-6 w-full h-[500px]">
        <form onSubmit={getDownloadFile}>
          <div className="flex flex-wrap items-end gap-8">
            <div className="space-y-2 text-lg md:text-2xl w-full md:w-1/4">
              {/* เเถวที่ 1 : Dropdown*/}

              <label htmlFor="select-option">คณะ</label>
              <select
                id="select-option"
                className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
              >
                <option value="computer">วิศวกรรมคอมพิวเตอร์</option>
                <option value="computerNext">วิศวกรรมไฟฟ้า</option>
              </select>
            </div>
            <div className="space-y-2 text-lg md:text-2xl w-full md:w-1/4">
              <label htmlFor="select-option">หลักสูตร</label>
              <select
                id="select-option"
                className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
              >
                <option value="computer">ปกติ</option>
                <option value="computerNext">ต่อเนื่อง</option>
              </select>
            </div>
            <div className=" text-lg md:text-2xl w-full md:w-2/4">
              <button
                type="download"
                className="text-white text-text-lg md:text-2xl px-4 py-2 rounded-lg bg-[#FF9D2E] hover:bg-[#F28204]"
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
              file:bg-[#FF9D2E] file:rounded-lg file:border-none file:px-4 file:py-2 file:text-white file:cursor-pointer file:mr-4"
              />
            </div>
            <div>
              <button
                type="submit"
                className="text-white text-lg md:text-2xl px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
              >
                พยากรณ์
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PredictStudent;

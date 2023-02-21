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
        <div className="flex flex-wrap items-end gap-8">
          <div className="space-y-2 text-lg md:text-2xl w-full md:w-1/4">
            <form onSubmit={handleSubmit}>
              {/* <select name='pred'>
          <option value="Grade">Predict By Grade</option>
          <option value="Class">Predict By Class</option>
        </select> */}
              <input type="file" accept=".csv" onChange={handleChange} />
              <button
                type="submit"
                className="bg-blue-500 px-4 py-2 rounded-md font-semibold"
              >
                fetch
              </button>
            </form>
            <br></br>
            <form onSubmit={getDownloadFile}>
              <select name="curri">
                <option value="computer">วิศวกรรมคอมพิวเตอร์</option>
                <option value="computerNext">
                  วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)
                </option>
              </select>
              <YearList></YearList>
              <button type="submit">
                Download CSV Format For subject 2560
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictStudent;

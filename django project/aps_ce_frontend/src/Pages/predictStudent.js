import React, { useState } from "react";
import axios from "axios";

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
    async function fetchData() {
      let res = await axios.post("http://localhost:8000/test", formData);
      console.log(res.data);
    }

    fetchData();
  };

  const getDownloadFile = (e) => {
    e.preventDefault();
    async function getfile() {
      let res = await axios({
        url: "http://localhost:8000/downloadCsv", //your url
        method: "GET",
        responseType: "blob", // important
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "APS_CE_Template.csv"); //or any other extension
        document.body.appendChild(link);
        link.click();
      });
    }
    getfile();
  };

  return (
    <div className="flex flex-col gap-6 justify-center items-center h-screen">
      <h1>File CSV Uploader</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleChange} />
        <button
          type="submit"
          className="bg-blue-500 px-4 py-2 rounded-md font-semibold"
        >
          fetch
        </button>
      </form>
      <br></br>
      <button onClick={getDownloadFile}>DownloadCSVFile</button>
    </div>
  );
};

export default PredictStudent;

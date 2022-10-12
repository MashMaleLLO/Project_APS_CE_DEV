import React, { useState } from "react";
import axios from "axios";

const ReqAna = () => {
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
      let res = await axios.post("http://localhost:8000/reqPredict", formData);
      console.log(res.data);
    }

    fetchData();
  };

  const getDownloadFile = (e) => {
    e.preventDefault();
    async function getfile() {
      let res = await axios({
        url: "http://localhost:8000/reqAna/" + e.target.curri.value, //your url
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
    <div className="flex flex-col gap-6 justify-center items-center h-screen">
      <h1>Upload your grade CSV (Save file as CSV-UTF-8)</h1>
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
      <form onSubmit={getDownloadFile}>
        <select name='curri'>
          <option value="computer">วิศวกรรมคอมพิวเตอร์</option>
          <option value="computerNext">วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)</option>
        </select>
        <button type="submit">Download CSV Format For subject 2560</button>
      </form>
      
    </div>
  );
};

export default ReqAna;

import React, { useState , useEffect } from "react";
import axios from "axios";

const DataUpload = () => {
  let formData = new FormData();
  const [csvFile, setCsvFile] = useState();
  const [dataType, setDataType] = useState("subjectData");

  if (csvFile) {
    formData.append("path_to_csv", csvFile);
  }

  const handleChange = (e) => {
    if (e.currentTarget.files) setCsvFile(e.currentTarget.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    async function fetchData() {
      let res = await axios.post("http://localhost:8000/fileUpload", formData);
      console.log(res.data);
    }

    fetchData();
  };

  useEffect(() => {
    if (dataType == "subjectData") {
      let res = axios.post("http://localhost:8000/getCareerResult/", formData);
    } else if (dataType == "studentData") {
      let res = axios.post("http://localhost:8000/getCareerResult/", formData);
    }
  }, [dataType]);

  const handleButtonClick = (type) => {
    setDataType(type);
  }

  return (
    <>
      <div>
        <button onClick={() => handleButtonClick("subjectData")}>
          Subject Data
        </button>
        <br></br>
        <button onClick={() => handleButtonClick("studentData")}>
          Student Data
        </button>
      </div>
      {dataType == "subjectData" ? (
        <div className="flex flex-col gap-6 justify-center items-center h-screen">
          <h1>File Subject Data Uploader</h1>
          <form onSubmit={handleSubmit}>
            <input type="file" accept=".csv" onChange={handleChange} />
            <button
              type="submit"
              className="bg-blue-500 px-4 py-2 rounded-md font-semibold"
            >
              fetch
            </button>
          </form>
        </div>
      ) : (
        <div className="flex flex-col gap-6 justify-center items-center h-screen">
          <h1>File Student Data Uploader</h1>
          <form onSubmit={handleSubmit}>
            <input type="file" accept=".csv" onChange={handleChange} />
            <button
              type="submit"
              className="bg-blue-500 px-4 py-2 rounded-md font-semibold"
            >
              fetch
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default DataUpload;

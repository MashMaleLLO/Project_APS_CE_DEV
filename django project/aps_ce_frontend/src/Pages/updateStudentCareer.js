import React, { useState } from "react";
import axios from "axios";

const CareerUpdate = () => {
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
      let res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/studentUpdateCareer`, formData);
      console.log(res.data);
    }

    fetchData();
  };

  return (
    <div className="flex flex-col gap-6 justify-center items-center h-screen">
      <h1>File Student Update Career Uploader</h1>
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
  );
};

export default CareerUpdate;

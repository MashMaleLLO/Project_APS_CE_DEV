import React, { useState, useEffect } from "react";
import axios from "axios";

const DataUpload = () => {
  let formData = new FormData();
  const [csvFile, setCsvFile] = useState();
  const [dataType, setDataType] = useState("ข้อมูลเกรดและนักศึกษา");
  const [data, setData] = useState([]);
  const [pageStudentData, setPageStudentData] = useState(false);
  const [filteredData, setFilteredData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get("http://localhost:8000/getFile");
      setData(response.data.message);
    }
    fetchData();
  }, []);

  if (csvFile) {
    formData.append("path_to_csv", csvFile);
  }

  const handleChange = (e) => {
    if (e.currentTarget.files) setCsvFile(e.currentTarget.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    formData.append("type_data", JSON.stringify(dataType)); // append the JSON object to the form data
    axios
      .post("http://localhost:8000/fileUpload", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // set the content type to multipart/form-data
        },
      })
      .then((res) => {
        console.log(res.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleDelete = (e, id) => {
    e.preventDefault();
    async function fetchData() {
      const response = await axios.delete(
        `http://localhost:8000/getFile?id=${id}`
      );
    }
    fetchData();
  };

  useEffect(() => {
    if (dataType === "ข้อมูลรายวิชา") {
      setFilteredData(
        data.filter((item) => item.type_data === "ข้อมูลรายวิชา")
      );
      setPageStudentData(false);
    } else if (dataType === "ข้อมูลเกรดและนักศึกษา") {
      setFilteredData(
        data.filter((item) => item.type_data === "ข้อมูลเกรดและนักศึกษา")
      );
      setPageStudentData(true);
    }
    console.log("หลังฟิล" + filteredData);
  }, [dataType, data]);

  const handleButtonClick = (type) => {
    setDataType(type);
  };

  return (
    <>
      <div>
        <button onClick={() => handleButtonClick("ข้อมูลรายวิชา")}>
          Subject Data
        </button>
        <br></br>
        <button onClick={() => handleButtonClick("ข้อมูลเกรดและนักศึกษา")}>
          Student Data
        </button>
      </div>
      {pageStudentData ? (
        <div className="flex flex-col gap-6 justify-center items-center h-screen">
          <h1>ข้อมูลในระบบ</h1>
          <form onSubmit={handleSubmit}>
            <input type="file" accept=".csv" onChange={handleChange} />
            <button
              type="submit"
              className="bg-blue-500 px-4 py-2 rounded-md font-semibold"
            >
              อัพโหลดไฟล์
            </button>
          </form>
          <ul>
            {filteredData.map((item) => (
              <div key={item.id}>
                <p>{item.name}</p>
                <button onClick={(e) => handleDelete(e, item.id)}>
                  Delete
                </button>
              </div>
            ))}
          </ul>
        </div>
      ) : (
        <div className="flex flex-col gap-6 justify-center items-center h-screen">
          <h1>ข้อมูลในระบบ</h1>
          <form onSubmit={handleSubmit}>
            <input type="file" accept=".csv" onChange={handleChange} />
            <button
              type="submit"
              className="bg-blue-500 px-4 py-2 rounded-md font-semibold"
            >
              อัพโหลดไฟล์
            </button>
          </form>
          <ul>
            {filteredData.map((item) => (
              <div key={item.id}>
                <p>{item.name}</p>
                <button onClick={(e) => handleDelete(e, item.id)}>
                  Delete
                </button>
              </div>
            ))}
          </ul>
        </div>
      )}
    </>
  );
};

export default DataUpload;

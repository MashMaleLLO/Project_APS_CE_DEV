import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const DataUpload = () => {
  let formData = new FormData();
  const [csvFile, setCsvFile] = useState();
  const [dataType, setDataType] = useState("ข้อมูลเกรดและนักศึกษา");
  const [data, setData] = useState([]);
  const [pageStudentData, setPageStudentData] = useState(false);
  const [filteredData, setFilteredData] = useState([]);
  const navigate = useNavigate();

  async function fetchData() {
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/getFile`);
    setData(response.data.message);
  }

  useEffect(() => {
    fetchData();
  }, []);

  if (csvFile) {
    formData.append("path_to_csv", csvFile);
  }

  const handleChange = (e) => {
    if (e.currentTarget.files) setCsvFile(e.currentTarget.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    formData.append("type_data", JSON.stringify(dataType)); // append the JSON object to the form data
    await axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/fileUpload`, formData, {
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
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/getFile`);
    setData(response.data.message);
  };

  const handleDelete = (e, id) => {
    console.log(id);
    e.preventDefault();
    if (window.confirm("คุณแน่ใจใช่ไหมว่าจะลบไฟล์")) {
      async function fetchData() {
        await axios.delete(`${process.env.REACT_APP_BACKEND_URL}/getFile/` + id);
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/getFile`);
        setData(response.data.message);
      }
      fetchData();
    }
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
    console.log("หลังฟิล", filteredData);
  }, [dataType, data]);

  const handleButtonClick = (type) => {
    setDataType(type);
  };

  const dataEdit = (item) => {
    console.log("ใช้edit", item);
    let dataEdit = `/dataEdit/${item}`;
    navigate(dataEdit);
  };


  return (
    <>
      <div className="w-full py-12">
        <div className="flex items-center justify-center">
          <button
            className={`${
              dataType === "ข้อมูลเกรดและนักศึกษา"
                ? "text-black"
                : "text-[#A7A7A7]"
            } text-xl md:text-2xl font-bold cursor-pointer py-4 px-4`}
            onClick={() => handleButtonClick("ข้อมูลเกรดและนักศึกษา")}
          >
            ข้อมูลนักศึกษา
          </button>
          <span className="text-xl md:text-2xl">|</span>
          <button
            className={`${
              dataType === "ข้อมูลรายวิชา" ? "text-black" : "text-[#A7A7A7]"
            } text-xl md:text-2xl font-bold cursor-pointer py-4 px-4`}
            onClick={() => handleButtonClick("ข้อมูลรายวิชา")}
          >
            หลักสูตรวิชา
          </button>
        </div>
      </div>
      {pageStudentData ? (
        <div className="flex flex-col mx-auto py-8 px-8 md:mb-20 md:px-32 xl:mb-36">
          <h1 className="py-6 text-xl md:text-2xl">ข้อมูลในระบบ</h1>
          <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-8 py-8 space-y-6 w-full ">
            <form onSubmit={handleSubmit}>
              <div className="flex gap-8">
                <div className="w-full md:w-[30%]">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleChange}
                    className="w-full px-4 py-1 text-gray-500 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none
              file:bg-[#FF9D2E] file:rounded-lg file:border-none file:px-2.5 file:py-1.5 file:text-white file:cursor-pointer file:mr-4"
                  />
                </div>

                <button
                  type="submit"
                  className="w-[120px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                >
                  อัพโหลดไฟล์
                </button>
              </div>
            </form>
            <div className="flex flex-col gap-2 px-4">
              {filteredData.map((item, index) => (
                <div
                  key={item.id}
                  className={`flex justify-between py-2 ${
                    index !== filteredData.length - 1
                      ? "border-b-[1.5px] border-[#A7A7A7]"
                      : ""
                  }`}
                >
                  <ol className="text-sm md:text-base">
                    <li key={index + 1}> {`${index + 1}. ${item.name}`}</li>
                  </ol>
                  <div className="flex items-end gap-4">
                    <div>
                      <button
                        className="w-full text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                        onClick={(e) => handleDelete(e, item.id)}
                      >
                        ลบ
                      </button>
                    </div>
                    <div>
                      <button
                        className="w-full text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                        onClick={() => dataEdit(item.id)}
                      >
                        แก้ไขไฟล์
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="flex flex-col mx-auto py-8 px-8 md:mb-20 md:px-32 xl:mb-36">
          <h1 className="py-6 text-xl md:text-2xl">ข้อมูลในระบบ</h1>
          <div className="container mx-auto flex flex-col rounded-lg drop-shadow-md bg-white px-8 py-8 space-y-6 w-full ">
            <form onSubmit={handleSubmit}>
              <div className="flex gap-8">
                <div className="w-full md:w-[30%]">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleChange}
                    className="w-full px-4 py-1 text-gray-500 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none
    file:bg-[#FF9D2E] file:rounded-lg file:border-none file:px-2.5 file:py-1.5 file:text-white file:cursor-pointer file:mr-4"
                  />
                </div>

                <button
                  type="submit"
                  className="w-[120px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                >
                  อัพโหลดไฟล์
                </button>
              </div>
            </form>
            <div className="flex flex-col gap-2 px-4">
              {filteredData.map((item, index) => (
                <div
                  key={item.id}
                  className={`flex justify-between py-2 ${
                    index !== filteredData.length - 1
                      ? "border-b-[1.5px] border-[#A7A7A7]"
                      : ""
                  }`}
                >
                  <ol className="text-sm md:text-base">
                    <li key={index + 1}> {`${index + 1}. ${item.name}`}</li>
                  </ol>
                  <div className="flex items-end gap-4">
                    <div>
                      <button
                        className="w-full text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                        onClick={(e) => handleDelete(e, item.id)}
                      >
                        ลบ
                      </button>
                    </div>
                    <div>
                      <button
                        className="w-full text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                        onClick={() => dataEdit(item.id)}
                      >
                        แก้ไขไฟล์
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DataUpload;

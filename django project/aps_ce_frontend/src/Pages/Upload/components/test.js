import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

const Test2 = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [data, setData] = useState([]);
  const [nameData, setNameData] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);

  const dataUpload = () => {
    let dataUpload = `/dataUpload`;
    navigate(dataUpload);
  };

  async function fetchData() {
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/getFile/` + id);
    console.log(response.data);
    setData(response.data.message.file_content);
    setNameData(response.data.message.file_information.name);
  }

  useEffect(() => {
    fetchData();
  }, []);

  const handleRowClick = (row) => {
    setSelectedRow(row);
  };

  const handleDelete = async (row) => {
    if (window.confirm("คุณแน่ใจใช่ไหมว่าจะลบไฟล์")) {
      await axios.put(`${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id, {
        action: "Delete",
        index: data.indexOf(row),
        content: {},
      });

      fetchData();
      setSelectedRow(null);
    }
  };

  const [isAddClicked, setIsAddClicked] = useState(false);
  const handleAddFormSubmit = async (event, content) => {
    event.preventDefault();
    await axios.put(`${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id, {
      action: "Add",
      index: "",
      content,
    });

    fetchData();
    setIsAddClicked(false);
  };

  const getClearedObject = (data) =>
    Object.fromEntries(Object.entries(data).map(([v]) => [v, ""]));

  const handleEditFormSubmit = async (event, content) => {
    event.preventDefault();
    await axios.put(`${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id, {
      action: "Edit",
      index: data.indexOf(selectedRow),
      content: content,
    });

    fetchData();
    setSelectedRow(null);
  };

  return (
    <>
      <div className="w-full">
        <h1 className="py-12 text-xl md:text-2xl font-bold">{nameData}</h1>
        <div className="flex flex-col mx-auto py-8 px-8 md:mb-20 md:px-32 xl:mb-36">
          <div>
            {isAddClicked ? (
              <Form
                label="Add"
                initValue={getClearedObject(data[0])}
                handleSubmit={handleAddFormSubmit}
              />
            ) : (
              <button
                type="button"
                onClick={() => setIsAddClicked((old) => !old)}
                className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
              >
                เพิ่มข้อมูล
              </button>
            )}
          </div>

          <table className="border-collapse border border-slate-400">
            <thead>
              <tr>
                <td className="border border-slate-300">
                  {data.length > 0 &&
                    Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
                </td>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr>

                <td key={index} onClick={() => handleRowClick(item)}>
                  {Object.keys(item).map((key) => (
                    <td key={key}>{item[key]}</td>
                  ))}
                  <td className="border border-slate-300 justify-evenly">
                    <button onClick={(e) => handleDelete(item)}>ลบ</button>
                  </td>
                </td>
                </tr>
              ))}
            </tbody>
          </table>
          {selectedRow && (
            <Form
              label={"Edit"}
              initValue={selectedRow}
              handleSubmit={handleEditFormSubmit}
            />
          )}
          <button onClick={dataUpload}>กลับ</button>
        </div>
      </div>
    </>
  );
};

const Form = ({ label, initValue, handleSubmit }) => {
  const [changedData, setChangedData] = useState(initValue);

  const onChange = (event) => {
    setChangedData((old) => ({
      ...old,
      [event.target.name]: event.target.value,
    }));
  };

  return (
    <form
      className="p-2 flex flex-col items-start gap-y-1"
      onSubmit={(e) => handleSubmit(e, changedData)}
    >
      <span className="text-xl font-bold">{label}</span>
      {Object.entries(initValue).map(([key, value]) => (
        <div key={key} className="flex items-center gap-x-2">
          <span className="">{key}</span> :
          <input
            className="!border-1 border-grey-500 px-2 py-1 rounded-md"
            type="text"
            onChange={onChange}
            name={key}
            value={value}
          />
        </div>
      ))}
      <button type="submit" className="border px-2">
        Save
      </button>
    </form>
  );
};

export default Test2;

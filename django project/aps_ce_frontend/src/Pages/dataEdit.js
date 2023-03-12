import React, { useState, useEffect } from "react";
import axios from "axios";
<<<<<<< HEAD
import { useNavigate , useParams} from "react-router-dom";

const DataEdit = () => {
  const navigate = useNavigate();
  const {id} = useParams();
  const [data, setData] = useState([]);
=======
import { useNavigate, useParams } from "react-router-dom";

const DataEdit = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [data, setData] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);
  const [editContent, setEditContent] = useState("");
>>>>>>> master

  const dataUpload = () => {
    let dataUpload = `/dataUpload`;
    navigate(dataUpload);
  };

  useEffect(() => {
    async function fetchData() {
<<<<<<< HEAD
      const response = await axios.get(`http://localhost:8000/getFile/`+id);
=======
      const response = await axios.get(`http://localhost:8000/getFile/` + id);
>>>>>>> master
      setData(response.data.message.file_content);
    }
    fetchData();
  }, []);

<<<<<<< HEAD
  console.log('ควย',data);

  return (
    <>
      <h1>สวัสดี</h1>
      <button onClick={dataUpload}>กลับ</button>
      {data.map((item) => (
                <p>{item.student_id}</p>
            ))}
=======
  const handleRowClick = (row) => {
    setSelectedRow(row);
  };

  const handleEditFormSubmit = async (event) => {
    event.preventDefault();

    console.log("index",data.indexOf(selectedRow));
    console.log("content",editContent);
    const response = await axios.put(`http://localhost:8000/editFileContent/${id}`, {
      action: "Edit",
      index: data.indexOf(selectedRow),
      content: editContent,
    });

    setData(response.data.message.file_content);
    setSelectedRow(null);
    setEditContent("");
  };

  return (
    <>
      <table>
        <thead>
          <tr>
            {data.length > 0 &&
              Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index} onClick={() => handleRowClick(item)}>
              {Object.keys(item).map((key) => (
                <td key={key}>{item[key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {selectedRow && (
        <div>
          <h2>Row Details</h2>
          <p>{JSON.stringify(selectedRow)}</p>
          <form onSubmit={handleEditFormSubmit}>
            <label>
              Edit content:
              <input
                type="text"
                value={editContent}
                onChange={(event) => setEditContent(event.target.value)}
              />
            </label>
            <button type="submit">Save</button>
          </form>
        </div>
      )}
      <button onClick={dataUpload}>กลับ</button>
>>>>>>> master
    </>
  );
};

<<<<<<< HEAD
export default DataEdit;
=======
export default DataEdit;
>>>>>>> master

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

const DataEdit = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [data, setData] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);
  const [editContent, setEditContent] = useState("");

  const dataUpload = () => {
    let dataUpload = `/dataUpload`;
    navigate(dataUpload);
  };

  async function fetchData() {
      const response = await axios.get(`http://localhost:8000/getFile/` + id);
      setData(response.data.message.file_content);
    }

  useEffect(() => {
    
    fetchData();
  }, []);
  

  const handleRowClick = (row) => {
    setSelectedRow(row);
  };

  const handleEditFormSubmit = async (event) => {
    event.preventDefault();

    console.log("index",data.indexOf(selectedRow));
    console.log("content",editContent);
    await axios.put(`http://localhost:8000/editFileContent/`+ id, {
      action: "Edit",
      index: data.indexOf(selectedRow),
      content: JSON.parse(editContent),
    });

    fetchData();

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
    </>
  );
};

export default DataEdit;
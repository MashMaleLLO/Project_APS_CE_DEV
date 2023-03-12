import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate , useParams} from "react-router-dom";

const DataEdit = () => {
  const navigate = useNavigate();
  const {id} = useParams();
  const [data, setData] = useState([]);

  const dataUpload = () => {
    let dataUpload = `/dataUpload`;
    navigate(dataUpload);
  };

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`http://localhost:8000/getFile/`+id);
      setData(response.data.message.file_content);
    }
    fetchData();
  }, []);

  console.log('ควย',data);

  return (
    <>
      <h1>สวัสดี</h1>
      <button onClick={dataUpload}>กลับ</button>
      {data.map((item) => (
                <p>{item.student_id}</p>
            ))}
    </>
  );
};

export default DataEdit;

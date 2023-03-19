import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
//import { useSnackbar } from "notistack";
import { Dialog } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";


const DeleteButton = () => {
 // const { enqueueSnackbar } = useSnackbar();
  const [open, setOpen] = useState(false);
  const [waiting, setWaiting] = useState(false);

  const handleClick = (isOpen) => () => {
    setOpen(isOpen);
  };

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
    const response = await axios.get(`http://localhost:8000/getFile/` + id);
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

  // const handleDelete = async (row) => {
  //   if (window.confirm("คุณแน่ใจใช่ไหมว่าจะลบไฟล์")) {
  //     await axios.put(`http://localhost:8000/editFileContent/` + id, {
  //       action: "Delete",
  //       index: data.indexOf(row),
  //       content: {},
  //     });
  //     fetchData();
  //     setSelectedRow(null);
  //   }
  // };

  const handleDelete = async (row) => {
      if (window.confirm("คุณแน่ใจใช่ไหมว่าจะลบไฟล์")) {
        await axios.put(`http://localhost:8000/editFileContent/` + id, {
          action: "Delete",
          index: data.indexOf(row),
          content: {},
          
        });
       // enqueueSnackbar('Delete Success', { variant: 'success' });
        fetchData();
        setSelectedRow(null);
      }
      setOpen(false);
    };

  return (
    <div>
           <button type="button" onClick={handleClick(true)}>
        <DeleteIcon className="group text-[#999999] hover:text-primary cursor-pointer" />
      </button>

      <Dialog
        open={open}
        onClose={handleClick(false)}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <div className="p-8 w-[32rem]">
        
            <>
              <h1 className="font-bold mb-4 text-xl">Delete</h1>
              <h4 className="mb-8 text-slate-600">
                Are you sure want to delete?
              </h4>
              <div className="flex justify-end gap-4">
                
                <button
                  type="button"
                  onClick={handleDelete}
                  className="px-5 py-2 text-white bg-red-500 rounded-lg font-semibold duration-300 hover:bg-red-600"
                >
                  Delete
                </button>
                <button
                  type="button"
                  onClick={handleClick(false)}
                  className="px-5 py-2 border border-slate-400 rounded-lg font-semibold duration-300 hover:border-black "
                >
                  Cancel
                </button>
              </div>
            </>
         
        </div>
      </Dialog>
    </div>
  );
};

export default DeleteButton;

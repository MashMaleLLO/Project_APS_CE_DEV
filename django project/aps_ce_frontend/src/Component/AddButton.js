import AddIcon from "@mui/icons-material/Add";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Dialog } from "@mui/material";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";

//use in file dataEdit
const AddButton = ({ onAdd }) => {
  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: "70vw",
    bgcolor: "background.paper",
    boxShadow: 24,
    p: 6,
    display: "block",
    borderRadius: "8px",
  };

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleAdd = () =>{
    onAdd();
    handleClose();
  }

  
  return (
    <div>
      <button
        type="button"
        onClick={handleOpen}
        className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204] cursor-pointer"
      >
        <AddIcon className="text-white"/>
        เพิ่มข้อมูล
      </button>

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <div className="flex flex-col justify-between">
            <div className="flex justify-between items-center">
              <h2 id="modal-modal-title" className="text-xs md:text-base">
                ehhr
              </h2>
              <p id="modal-modal-description" className="text-xs md:text-base">
                รหัสวิชา 
              </p>
            </div>
            <p
              id="modal-modal-description"
              className="pt-6 text-xs md:text-base"
            >
              รายละเอียดวิชา
            </p>
            <div className="flex justify-center items-end pt-6">
              <button
                type="close"
                onClick={handleAdd}
                className="w-[70px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
              >
                ยืนยัน
              </button>
            </div>
          </div>
        </Box>
      </Modal>
    </div>
  );
};

export default AddButton;

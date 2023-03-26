import AddIcon from "@mui/icons-material/Add";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Dialog } from "@mui/material";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";

//use in file dataEdit
const AddButton = ({ addForm }) => {
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

  const handleAdd = () => {
    addForm();
    handleClose();
  };
  
  
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
          {addForm()}
        </Box>
      </Modal>
    </div>
  );
};

export default AddButton;
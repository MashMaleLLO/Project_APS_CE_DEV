import DeleteIcon from "@mui/icons-material/Delete";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
import { Dialog } from "@mui/material";

//use in file dataEdit
const DeleteButton = ({ onDelete }) => {
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleDelete = () => {
    onDelete();
    handleClose();
  };

  return (
    <div>
      <button type="button" onClick={handleClickOpen}>
        <DeleteIcon className="group text-[#999999] hover:text-primary cursor-pointer" />
      </button>

      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <div className="p-8 w-[32rem]">
          <h1 className="font-bold mb-4 text-xl">Delete</h1>
          <h4 className="mb-8 text-slate-600">
            คุณต้องการที่จะลบไฟล์นี้หรือไม่
          </h4>
          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={handleDelete}
              className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204] cursor-pointer"
            >
              ลบ
            </button>
            <button
              type="button"
              onClick={handleClose}
              className="text-[#999999] font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 cursor-pointer"
            >
              ยกเลิก
            </button>
          </div>
        </div>
      </Dialog>
    </div>
  );
};

export default DeleteButton;
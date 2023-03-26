import AddIcon from "@mui/icons-material/Add";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Dialog } from "@mui/material";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";

//use in file dataEdit
const AddButton = ({ onClick }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204] cursor-pointer"
    >
      <AddIcon className="text-white" />
      เพิ่มข้อมูล
    </button>
  );
};

export default AddButton;

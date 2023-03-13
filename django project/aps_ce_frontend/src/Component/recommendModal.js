import React, { useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";

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

export default function RecommendModal({ subjects }) {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  console.log("modal", subjects);

  return (
    <div>
      <Button onClick={handleOpen}>
        <div className="flex text-[#999999] text-sm md:text-base bg-[#FFD670] p-2 rounded-lg">
          ดูรายละเอียด
        </div>
      </Button>
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
                {subjects?.subject_name_eng}
              </h2>
              <p id="modal-modal-description" className="text-xs md:text-base">
                รหัสวิชา : {subjects?.subject_id}
              </p>
            </div>
            <p
              id="modal-modal-description"
              className="pt-6 text-xs md:text-base"
            >
              รายละเอียดวิชา : {subjects?.abstract}
            </p>
            <div className="flex justify-center items-end pt-6">
              <button
                type="close"
                onClick={handleClose}
                className="w-[70px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
              >
                ปิด
              </button>
            </div>
          </div>
        </Box>
      </Modal>
    </div>
  );
}

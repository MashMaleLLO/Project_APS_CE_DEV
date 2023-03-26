import { useState, useImperativeHandle, forwardRef } from "react";
import { Modal, Box } from "@mui/material";
import { useParams } from "react-router-dom";

import axios from "axios";
import useAddData from "../hooks/useAddData";

const AddForm = forwardRef((_, ref) => {
  const { data, addData, onChange } = useAddData();

  if (!data) return null;

  const BoxStyle = {
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

  const [isOpen, setIsOpen] = useState(false);

  useImperativeHandle(ref, () => ({
    open: () => {
      console.log("set");
      setIsOpen(true);
    },
    close: () => {
      setIsOpen(false);
    },
  }));

  const handleSubmit = (e) => {
    e.preventDefault();
    addData();
  };

  return (
    <Modal
      open={isOpen}
      onClose={() => setIsOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box style={BoxStyle}>
        <form
          className="p-2 flex flex-col items-start gap-y-1"
          onSubmit={(e) => addData(e, changedData)}
        >
          {Object.entries(formObject).map(([key, value]) => (
            <div key={key} className="flex items-center gap-x-2">
              <span className="">{key}</span> :
              <input
                className="!border-1 border-grey-500 px-2 py-1 rounded-md"
                type="text"
                onChange={onChange}
                name={key}
              />
            </div>
          ))}
          <button type="submit" className="border px-2">
            Save
          </button>
        </form>
      </Box>
    </Modal>
  );
});

export default AddForm;

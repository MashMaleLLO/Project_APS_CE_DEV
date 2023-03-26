import { useState, useImperativeHandle, forwardRef } from "react";
import { Modal, Box } from "@mui/material";
import { useParams } from "react-router-dom";

import axios from "axios";
import useAddData from "../../hooks/useAddData";

const AddFormModal = forwardRef((_, ref) => {
  const { data, addData, onChange } = useAddData();

  const [isOpen, setIsOpen] = useState(false);
  useImperativeHandle(ref, () => ({
    open: () => {
      setIsOpen(true);
    },
    close: () => {
      setIsOpen(false);
    },
  }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addData();
    setIsOpen(false);
  };

  return (
    <Modal
      open={isOpen}
      onClose={() => setIsOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white">
        <form
          className="p-2 flex flex-col items-start gap-y-1"
          onSubmit={handleSubmit}
        >
          {data[0] &&
            Object.entries(data[0]).map(([key, value]) =>
              key === "index" ? null : (
                <div key={key} className="flex items-center gap-x-2">
                  <span className="">{key}</span> :
                  <input
                    className="!border-1 border-grey-500 px-2 py-1 rounded-md"
                    type="text"
                    onChange={onChange}
                    name={key}
                  />
                </div>
              )
            )}
          <button type="submit" className="border px-2">
            Save
          </button>
        </form>
      </div>
    </Modal>
  );
});

export default AddFormModal;

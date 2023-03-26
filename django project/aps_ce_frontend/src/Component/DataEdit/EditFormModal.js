import { useState, useImperativeHandle, forwardRef } from "react";
import { Modal, Box } from "@mui/material";
import { useParams } from "react-router-dom";

import axios from "axios";
import useEditData from "../../hooks/useEditData";

const EditFormModal = forwardRef((_, ref) => {
  const { selectedEditRow, clearSelectedEditRow, onChange, editData } =
    useEditData();

  const handleSubmit = (e) => {
    e.preventDefault();
    editData();
  };

  return (
    <Modal
      open={selectedEditRow}
      onClose={clearSelectedEditRow}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white">
        <form
          className="p-2 flex flex-col items-start gap-y-1"
          onSubmit={handleSubmit}
        >
          {selectedEditRow &&
            Object.entries(selectedEditRow).map(([key, value]) =>
              key === "index" ? null : (
                <div key={key} className="flex items-center gap-x-2">
                  <span className="">{key}</span> :
                  <input
                    className="bg-green-300 border-1 border-grey-500 px-2 py-1 rounded-md"
                    type="text"
                    onChange={onChange}
                    name={key}
                    defaultValue={value}
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

export default EditFormModal;

import { useState, useImperativeHandle, forwardRef } from "react";
import { Modal, Box } from "@mui/material";
import useEditData from "../../hooks/useEditData";

//modal edit form
const EditFormModal = forwardRef((_, ref) => {
  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: "50vw",
    bgcolor: "background.paper",
    boxShadow: 24,
    p: 6,
    display: "block",
    borderRadius: "8px",
  };

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
      <Box sx={style}>
        <form className="flex flex-col p-2 gap-y-2" onSubmit={handleSubmit}>
          <h1 className="font-bold mb-4 text-xl">Edit</h1>
          {selectedEditRow &&
            Object.entries(selectedEditRow).map(([key, value]) =>
              key === "index" ? null : (
                <div key={key} className="flex items-center gap-x-2">
                  <span className="">{key}</span> :
                  <input
                    className="w-full px-4 py-1 text-gray-500 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                    type="text"
                    onChange={onChange}
                    name={key}
                    defaultValue={value}
                  />
                </div>
              )
            )}
          <div className="flex items-center justify-center gap-4">
            <button
              type="submit"
              className="w-[80px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204] cursor-pointer"
            >
              Save
            </button>
          </div>
        </form>
      </Box>
      {/* <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white">
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
      </div> */}
    </Modal>
  );
});

export default EditFormModal;
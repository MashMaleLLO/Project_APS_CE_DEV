import { useState, useImperativeHandle, forwardRef } from "react";
import { Modal, Box } from "@mui/material";
import { useParams } from 'react-router-dom'

import axios from "axios";

const AddForm = forwardRef(({ formObject }, ref) => {
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
  const { id } = useParams();

  useImperativeHandle(ref, () => ({
    open: () => {
        console.log("set")
      setIsOpen(true);
    },
    close: () => {
        setIsOpen(false);
    },
}));

  const [changedData, setChangedData] = useState(formObject);

  const onChange = (event) => {
    setChangedData((old) => ({
      ...old,
      [event.target.name]: event.target.value,
    }));
  };

  const handleSubmit = async (event, content) => {
    event.preventDefault();
    await axios.put(`${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id, {
      action: "Add",
      index: "",
      content: content,
    });

    // fetchData();
    // setSelectedRow(null);
  };

  return (

    <Modal
      open={isOpen}
      onClose={()=> setIsOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
        <div>awdawdawdawdawdawdaad {isOpen ? "wadaw" : "dddd"}</div>
      {/* <Box style={BoxStyle}>
        <form
          className="p-2 flex flex-col items-start gap-y-1"
          onSubmit={(e) => handleSubmit(e, changedData)}
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
      </Box> */}
    </Modal>
  );
});

export default AddForm;

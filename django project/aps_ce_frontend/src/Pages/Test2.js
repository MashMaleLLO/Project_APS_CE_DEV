import React, { useState, useEffect } from "react";
import { DataGrid } from "@mui/x-data-grid";

const rows = [
  { id: 1, name: "John Doe", age: 35, email: "johndoe@example.com" },
  { id: 2, name: "Jane Doe", age: 30, email: "janedoe@example.com" },
];

const Test2 = () => {
  const [editRowsModel, setEditRowsModel] = useState({});
  const [data, setData] = useState(rows);
  const [originalData, setOriginalData] = useState(rows);

  useEffect(() => {
    setOriginalData(data);
  }, [data]);

  const handleCellEditCommit = (params) => {
    if (Object.keys(editRowsModel).length === 0) {
      return; // exit early if editRowsModel is empty
    }
    const updatedRows = [...data];
    updatedRows[params.id - 1][params.field] = params.value;
    setData(updatedRows);
  };

  const handleEditButtonClick = () => {
    const ids = Object.keys(editRowsModel);
    if (ids.length === 0) {
      setEditRowsModel({ 1: true });
    } else {
      setEditRowsModel({});
      setData(originalData);
    }
  };

  const columns = [
    {
      field: "id",
      headerName: "ID",
      width: 70,
      editable: false,
    },
    {
      field: "name",
      headerName: "Name",
      width: 150,
      editable: true,
    },
    {
      field: "age",
      headerName: "Age",
      type: "number",
      width: 70,
      editable: true,
    },
    {
      field: "email",
      headerName: "Email",
      width: 250,
      editable: true,
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 250,
      renderCell: (params) => {
        return (
          <div className="flex flex-row space-x-4 items-center">
            <button onClick={handleEditButtonClick}>
              {Object.keys(editRowsModel).length === 0 ? "Edit" : "Cancel"}
            </button>
          </div>
        );
      },
    },
  ];

  return (
    <div>
      <div style={{ height: 400, width: "100%" }}>
        <DataGrid
          rows={data}
          columns={columns}
          pageSize={5}
          checkboxSelection
          editRowsModel={editRowsModel}
          onCellEditCommit={handleCellEditCommit}
        />
      </div>
    </div>
  );
};

export default Test2;

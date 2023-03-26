import React, { useState, useEffect } from "react";
import axios from "axios";
import { DataGrid, GridCellModes } from "@mui/x-data-grid";
import { useNavigate, useParams, GridColDef } from "react-router-dom";
import { capitalize } from "@mui/material";
import Table from "../Component/Table";
import DeleteButton from "../Component/DeleteButton";
import AddButton from "../Component/AddButton";
import EditButton from "../Component/EditButton";

const DataEdit = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [data, setData] = useState([]);
  const [nameData, setNameData] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);

  const dataUpload = () => {
    let dataUpload = `/dataUpload`;
    navigate(dataUpload);
  };

  const fetchData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/getFile/` + id);
      const data = response.data.message.file_content.map((row, index) => ({
        ...row,
        index: index + 1,
      }));
      setData(data);
      setNameData(response.data.message.file_information.name);
      console.log("Fetched data:", data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRowClick = (row) => {
    setSelectedRow(row);
  };

  const handleDelete = async (row) => {
    await axios.put(`http://localhost:8000/editFileContent/` + id, {
      action: "Delete",
      index: data.indexOf(row),
      content: {},
    });
    fetchData();
    setSelectedRow(null);
  };

const [isAddClicked, setIsAddClicked] = useState(false);
  const handleAddFormSubmit = async (event, content) => {
    event.preventDefault();
    await axios.put(`http://localhost:8000/editFileContent/` + id, {
      action: "Add",
      index: "",
      content: content,
    });

    fetchData();
    setSelectedRow(null);
  };

  const getClearedObject = (data) =>
    Object.fromEntries(Object.entries(data).map(([v]) => [v, ""]));

  const handleEditFormSubmit = async (event, content) => {
    event.preventDefault();
    await axios.put(`http://localhost:8000/editFileContent/` + id, {
      action: "Edit",
      index: data.indexOf(),
      content: content,
    });

    fetchData();
    setSelectedRow(null);
  };

  console.log("testdata", data);

  const addForm = () => {
    return (
      <div className="bg-green-300 flex flex-col">
                 {isAddClicked ? (
              <Form
                label="Add"
                initValue={getClearedObject(data[0])}
                handleSubmit={handleAddFormSubmit}
              />
            ) : (
              <button
                type="button"
                onClick={() => setIsAddClicked((old) => !old)}
                className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
              >
                เพิ่มข้อมูล
              </button>
            )}
       
      </div>
    );
  };
  console.log(addForm);

  const columns =
    data.length > 0
      ? [
          ...Object.keys(data[0]).map((key) => ({
            field: key,
            headerName: key,
            width: 150,
          })),
          {
            field: "Action",
            width: 150,
            headerName: "Action",
            editable: true,
            renderCell: (params) => {
              return (
                <div className="flex flex-row space-x-4 items-center">
                  {/* <EditButton onAdd={() => handleEditCellChange()} /> */}
                  <DeleteButton onDelete={() => handleDelete(params.row)} />
                  {/* <EditButton onClick={() => handleAdd(params.row)}>
                    edit
                  </EditButton> */}
                </div>
              );
            },
          },
        ]
      : [];

  return (
    <>
      {/* <div className="w-full">
        <h1 className="py-12 text-xl md:text-2xl font-bold">{nameData}</h1>
        <div className="flex flex-col mx-auto py-8 px-8 md:mb-20 md:px-32 xl:mb-36">
          <div>
            {isAddClicked ? (
              <Form
                label="Add"
                initValue={getClearedObject(data[0])}
                handleSubmit={handleAddFormSubmit}
              />
            ) : (
              <button
                type="button"
                onClick={() => setIsAddClicked((old) => !old)}
                className="text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
              >
                เพิ่มข้อมูล
              </button>
            )}
          </div>

          <table className="border-collapse border border-slate-400">
            <thead>
              <tr>
                <td className="border border-slate-300">
                  {data.length > 0 &&
                    Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
                </td>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr>
                  <td key={index} onClick={() => handleRowClick(item)}>
                    {Object.keys(item).map((key) => (
                      <td key={key}>{item[key]}</td>
                    ))}
                    <td className="">
                      <button onClick={(e) => handleDelete(item)}>ลบ</button>
                    </td>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {selectedRow && (
            <Form
              label={"Edit"}
              initValue={selectedRow}
              handleSubmit={handleEditFormSubmit}
            />
          )}
          <button onClick={dataUpload}>กลับ</button>
        </div>
      </div> */}

      <div className="flex flex-col h-full">
        <div className="container mx-auto py-8 px-8 md:px-32">
          <div className="flex justify-between py-6">
            <h1 className="text-xl md:text-2xl font-bold">{nameData}</h1>
            <AddButton addForm={addForm} />
          </div>

          <div className="w-full h-[450px] xl:h-[600px] py-8">
            {/* <Table
              columns={columns}
              rows={data}
            /> */}
            <DataGrid
              rows={data}
              columns={columns}
              getRowId={(row) => row?.index}
              autoHeight={false}
              rowHeight={60}
              pageSize={10}
              checkboxSelection
            
            />
          </div>
        </div>
      </div>
    </>
  );
};

const Form = ({ label, initValue, handleSubmit }) => {
  const [changedData, setChangedData] = useState(initValue);

  const onChange = (event) => {
    setChangedData((old) => ({
      ...old,
      [event.target.name]: event.target.value,
    }));
  };

  return (
    <form
      className="p-2 flex flex-col items-start gap-y-1"
      onSubmit={(e) => handleSubmit(e, changedData)}
    >
      <span className="text-xl font-bold">{label}</span>
      {Object.entries(initValue).map(([key, value]) => (
        <div key={key} className="flex items-center gap-x-2">
          <span className="">{key}</span> :
          <input
            className="!border-1 border-grey-500 px-2 py-1 rounded-md"
            type="text"
            onChange={onChange}
            name={key}
            value={value.grade}
          />
        </div>
      ))}
      <button type="submit" className="border px-2">
        Save
      </button>
    </form>
  );
};

export default DataEdit;

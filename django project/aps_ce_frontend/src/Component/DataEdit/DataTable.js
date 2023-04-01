import { useMemo, useState } from "react";
import { DataGrid, GridCellModes, useGridApiRef } from "@mui/x-data-grid";
import EditButton from "./EditButton";
import DeleteButton from "./DeleteButton";
import useDeleteData from "../../hooks/useDeleteData";
import useEditData from "../../hooks/useEditData";
import { generateUniqueId } from "../../utils/getUUID";

const DataTable = () => {
  const { deleteData, data } = useDeleteData();
  const { selectEditRow } = useEditData();
  const apiRef = useGridApiRef();
  console.log(data);
  const dataWithIndex = useMemo(
    () =>
      data.map((e, index) => ({
        ...e,
        index: index,
      })),
    [data]
  );

  const columns =
    dataWithIndex.length > 0
      ? [
          {
            field: "id",
            headerName: "Index",
            width: 80,
            renderCell: (params) => params.row.index + 1,
          },
          ...Object.keys(data[0]).map((key) => ({
            field: key,
            headerName: key,
            width: 170,
          })),
          {
            field: "Action",
            width: 100,
            headerName: "Action",
            editable: true,
            renderCell: (params) => {
              return (
                <div className="flex flex-row space-x-4 items-center">
                  <DeleteButton onDelete={() => deleteData(params.row.index)} />
                  <EditButton onClick={() => selectEditRow(params.row)} />
                  {/* <div
                    onClick={() => selectEditRow(params.row)}
                    className="flex flex-row space-x-4 items-center"
                  >
                    edit
                  </div> */}
                </div>
              );
            },
          },
        ]
      : [];

  return (
    <div className="w-full h-[450px] xl:h-[600px] py-8">
      <DataGrid
        apiRef={apiRef}
        rows={dataWithIndex}
        columns={columns}
        getRowId={(row) => row?.index}
        autoHeight={false}
        rowHeight={60}
        pageSize={10}
      />
      {/* <button onClick={() => console.log(apiRef.current.getSelectedRows())}>
        click test{" "}
      </button> */}
    </div>
  );
};

export default DataTable;
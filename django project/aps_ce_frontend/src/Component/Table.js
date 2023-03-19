import { DataGrid, GridColDef } from "@mui/x-data-grid";

const Table = ({ rows, columns }) => {
  return (
    <DataGrid
      rows={rows}
      columns={columns}
      getRowId={(row) => row?.index}
      autoHeight={false}
      rowHeight={60}
      sx={{
        boxShadow:
          "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.05)",
        borderRadius: "16px",
        padding: "12px",
      }}
    />
  );
};

export default Table;

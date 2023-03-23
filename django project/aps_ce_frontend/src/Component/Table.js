import { DataGrid, GridColDef } from "@mui/x-data-grid";

//use in file DataEdit
const Table = ({ rows, columns, onRowClick, editable}) => {
  return (
    <DataGrid
      columns={columns}
      rows={rows}
      getRowId={(row) => row?.index}
      autoHeight={false}
      rowHeight={60}
      experimentalFeatures={{ newEditingApi: true }}
      onRowClick={handleRowClick}
      editable={{
        onEditCellChange: handleEditCellChange,
        isCellEditable: () => true,
      }}
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

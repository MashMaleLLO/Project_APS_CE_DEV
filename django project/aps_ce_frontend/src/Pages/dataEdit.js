import React, { useState, useEffect, useRef, useContext } from "react";
import { useParams, GridColDef } from "react-router-dom";
import AddButton from "../Component/DataEdit/AddButton";
import AddFormModal from "../Component/DataEdit/AddFormModal";
import EditFormModal from "../Component/DataEdit/EditFormModal";
import DataTable from "../Component/DataEdit/DataTable";
import { DataEditProvider, DataEditContext } from "../Contexts/DataEditContext";

const DataEdit = () => {
  const { data, dataName } = useContext(DataEditContext);
  const addFormRef = useRef(null);

  return (
    <div className="flex flex-col h-full">
      {data && <AddFormModal ref={addFormRef} />}
      {data && <EditFormModal />}
      <div className="container w-full mx-auto py-8 px-8 md:px-32">
        <div className="flex w-full justify-between items-center py-6">
          <h1 className="text-xl md:text-2xl font-bold">{dataName}</h1>
          <AddButton onClick={() => addFormRef.current.open()} />
        </div>
        {data && <DataTable />}
      </div>
    </div>
  );
};

const WithProvider = () => {
  return (
    <DataEditProvider>
      <DataEdit />
    </DataEditProvider>
  );
};

export default WithProvider;
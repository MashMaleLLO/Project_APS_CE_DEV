import axios from "axios";
import React, { useState, useEffect, useRef, useContext } from "react";
import { useNavigate, useParams, GridColDef } from "react-router-dom";

import Table from "../Component/Table";

import AddButton from "../Component/DataEdit/AddButton";
import AddFormModal from "../Component/DataEdit/AddFormModal";
import EditFormModal from "../Component/DataEdit/EditFormModal";
import DataTable from "../Component/DataEdit/DataTable";

import { DataEditProvider, DataEditContext } from "../Contexts/DataEditContext";

const DataEdit = () => {
  const navigate = useNavigate();
  const { data } = useContext(DataEditContext);
  const { id } = useParams();
  const addFormRef = useRef(null);

  return (
    <div className="flex flex-col h-full">
      {data && <AddFormModal ref={addFormRef} />}
      {data && <EditFormModal />}
      <div className="container w-full mx-auto py-8 px-8 md:px-32">
        <div className="flex w-full justify-between py-6">
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

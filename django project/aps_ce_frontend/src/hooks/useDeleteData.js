import axios from "axios";
import { useContext } from "react";
import { useParams } from "react-router-dom";
import { DataEditContext } from "../Contexts/DataEditContext";

const useDeleteData = () => {
  const state = useContext(DataEditContext);
  const { data, fetchData } = state;
  const { id } = useParams();

  const deleteData = async (deleteId) => {
    console.log(deleteId);
    await axios.put(
      `${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id,
      {
        action: "Delete",
        index: deleteId,
        content: {},
      }
    );
    fetchData();
  };
  return { ...state, deleteData };
};

export default useDeleteData;

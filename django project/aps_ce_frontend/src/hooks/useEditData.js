import axios from "axios";
import { useContext, useCallback, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { DataEditContext } from "../Contexts/DataEditContext";

const useEditData = () => {
  const { selectedEditRow, setSelectedEditRow, data, fetchData } = useContext(DataEditContext);
  const [changedData, setChangedData] = useState();
  const { id } = useParams();

  useEffect(() => {
    setChangedData(selectedEditRow);
  }, [selectedEditRow]);
  const onChange = (event) => {
    setChangedData((old) => ({
      ...old,
      [event.target.name]: event.target.value,
    }));
  };

  const selectEditRow = (row) => {
    setSelectedEditRow(row);
  };

  const clearSelectedEditRow = () => {
    setSelectedEditRow(null);
  };

  const editData = useCallback(async () => {
    const { index, ...rest } = changedData;
    const { data: resposeData } = await axios.put(
      `${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id,
      {
        action: "Edit",
        index,
        content: rest,
      }
    );

    console.log(rest, resposeData.message);
    await fetchData();
    setSelectedEditRow(null);
  });

  return {
    selectedEditRow,
    selectEditRow,
    clearSelectedEditRow,
    onChange,
    editData,
  };
};

export default useEditData;

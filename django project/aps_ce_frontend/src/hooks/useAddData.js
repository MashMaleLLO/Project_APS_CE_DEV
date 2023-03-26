import axios from "axios";
import { useContext, useCallback, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { DataEditContext } from "../Contexts/DataEditContext";


const useAddData = () => {
  const addDataState = useContext(DataEditContext);
  const { data, fetchData } = addDataState;
  const { id } = useParams();

  const [changedData, setChangedData] = useState(data[0] || {});
  useEffect(() => {
    if (data?.[0]) {
      setChangedData(data[0]);
    }
  }, [data]);
  const onChange = (event) => {
    setChangedData((old) => ({
      ...old,
      [event.target.name]: event.target.value,
    }));
  };

  const addData = useCallback(async () => {
    const { index, ...rest } = changedData;
    await axios.put(
      `${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id,
      {
        action: "Add",
        index: "",
        content: rest,
      }
    );

    await fetchData();
  });

  return { ...addDataState, addData, onChange };
};

export default useAddData;

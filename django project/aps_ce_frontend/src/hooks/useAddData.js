import { useContext, useCallback } from "react";
import { useParams } from "react-router-dom";
import { DataEditContext } from "../Contexts/DataEditContext";

const useAddData = () => {
  const addDataState = useContext(DataEditContext);
  const { dataName, error, data, isLoading, fetchData } = addDataState;
  const { id } = useParams();

  const [changedData, setChangedData] = useState(formObject);

  const onChange = (event) => {
    setChangedData((old) => ({
      ...old,
      [event.target.name]: event.target.value,
    }));
  };

  const addData = useCallback(async () => {
    await axios.put(
      `${process.env.REACT_APP_BACKEND_URL}/editFileContent/` + id,
      {
        action: "Add",
        index: "",
        content: changedData,
      }
    );

    fetchData();
  });

  return { ...addDataState, addData, onChange };
};

export default useAddData;

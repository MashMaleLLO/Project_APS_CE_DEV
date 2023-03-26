import { useContext } from "react";
import { DataEditContext } from "../Contexts/DataEditContext";

const useDeleteData = () => {
  const addDataState = useContext(DataEditContext);
  const { dataName, error, fetchedData, isLoading } = addDataState;

    const handleAddData = ()=> {
        
    }

  return { ...addDataState }

};

export default useDeleteData
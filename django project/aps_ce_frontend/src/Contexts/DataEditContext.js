import { createContext, useState, useCallback, useEffect } from "react";

import { useParams } from "react-router-dom";
import axios from "axios";

export const DataEditContext = createContext({
  dataName: null,
  data: [],
  isLoading: false,
  error: null,
  fetchData: () => {},
  selectedEditRow: null,
  setSelectedEditRow: () => {},
});

export const DataEditProvider = ({ children }) => {
  const [data, setFetchedData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dataName, setDataName] = useState();

  const [selectedEditRow, setSelectedEditRow] = useState(null);

  const { id } = useParams();

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/getFile/` + id
      );
      const data = response.data.message.file_content.map((row, index) => ({
        ...row,
      }));
      setIsLoading(false);
      setFetchedData(data);
      setDataName(response.data.message.file_information.name);
    } catch (error) {
      const errorMsg =
        error instanceof Error ? error.message : "เกิดข้อผิดพลาด";
      setError(errorMsg);
    }
  }, [id]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <DataEditContext.Provider
      value={{
        error,
        selectedEditRow,
        setSelectedEditRow,
        data,
        isLoading,
        dataName,
        fetchData,
      }}
    >
      {children}
    </DataEditContext.Provider>
  );
};

import { createContext, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const DataEditContext = createContext({
  dataName: null,
  fetchedData: [],
  isLoading: false,
  error: null,
});

export const DataEditProvider = ({ children }) => {
  const [fetchedData, setFetchedData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dataName, setDataName] = useState();

  const { id } = useParams();

  useEffect(() => {
    const fetch = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/getFile/` + id);
        const data = response.data.message.file_content.map((row, index) => ({
          ...row,
          index: index + 1,
        }));
        setIsLoading(false);
        setFetchedData(data);
        setDataName(response.data.message.file_information.name);
      } catch (error) {
        const errorMsg =
          error instanceof Error ? error.message : "เกิดข้อผิดพลาด";
        setError(errorMsg);
      }
    };
    fetch();
  }, []);

  return (
    <DataEditContext.Provider value={{ error, fetchedData, isLoading }}>
      {children}
    </DataEditContext.Provider>
  );
};

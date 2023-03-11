import React, { useState, useEffect } from "react";
import { BarChart } from './BarChart'
import axios from 'axios';
import { Loading } from "./Looding";

//คาดการณ์สถิติบัณฑิต
const PredictCareer = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [labels, setLabels] = useState([]);
  const [year, setYear] = useState("2562");
  const jobData = Object.values(data);

  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      const response = await axios.post("http://localhost:8000/req_pred_many",{
        curriculum : "วิศวกรรมคอมพิวเตอร์",
        year : year
      });
      setData(response.data.message);
      setLabels(Object.keys(response.data.message));
      console.log("โชว์ดาต้า"+data);
      setLoading(false);
    }
    fetchData();
  }, [year]);

  const handleYearChange = (e) => {
    setYear(e.target.value);
  };

  console.log("labels:", labels);
  console.log("jobData:", jobData);

  //เอา MockData มา map
  const showGraph = {
    labels: labels,
    datasets: [
      {
        label: "สายงาน",
        //data: jobData.map((item) => item.Num_of_student),
        data: jobData.map((item) => item.Num_of_student),
        backgroundColor: ["#FFD670"],
      },
    ],
  };

  if (loading) return <Loading />;

  return (
    <div>
       {/* {loading ? (
        <div><Loading/></div>
      ) : ( */}

    <div className="flex flex-col items-center py-8">
      <div className="rounded-lg bg-white md:px-8">
        <div className="flex items-center justify-center pt-6">
          <div className="flex flex-row text-base md:text-lg w-[250px]">
            <span className="w-full flex items-center justify-center">
              ปีการศึกษา
            </span>
            <select
              id="select-option"
              value={year}
              onChange={handleYearChange}
              className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
            >
              <option value="2560">2560</option>
              <option value="2561">2561</option>
              <option value="2562">2562</option>
            </select>
          </div>
        </div>
        <BarChart chartData={showGraph} />

        <div className="flex items-center justify-between flex-wrap gap-4 px-4 py-8 lg:px-72 w-full lg:w-[1200px]">
          <div className="flex flex-col space-y-2">
            <h1 className="font-semibold text:xs md:text-base">สายงาน</h1>
            {labels.map((item, index) => (
              <h1 key={index} className="capitalize text:xs md:text-base">
                {item}
              </h1>
            ))}
          </div>

          <div className="flex flex-col space-y-2">
            <h1 className="font-semibold text:xs md:text-base">จำนวน</h1>
            {jobData.map((item, index) => (
              <h1 key={index} className="text:xs md:text-base">
                {item.Num_of_student}
              </h1>
            ))}
          </div>
        </div>
      </div>
      </div>
        {/* )}  */}
    </div>
  );
};

export default PredictCareer;
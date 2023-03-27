import React, { useState } from "react";
import PredictStudent from "./predictStudent";

const ResultPredict = ({ year, predicts }) => {
  
  const [back, setBack] = useState(false);

  const career = predicts.message.at(-1);

  return (
    <>
      {back ? (
        <PredictStudent />
      ) : (
        <form onSubmit={() => setBack(true)}>
          <div className="flex flex-col min-h-screen justify-between">
            <div className="container mx-auto py-8 px-8 md:px-32">
              <h1 className="py-12 text-xl md:text-2xl font-bold">
                ผลการวิเคราะห์
              </h1>
              <div className="container mx-auto rounded-lg drop-shadow-md bg-white px-4 py-8 space-y-6 w-full ">
                <h1 className="text-xs md:text-base">
                  คณะวิศวกรรมศาสตร์คอมพิวเตอร์ หลักสูตรปี {year}
                </h1>
                <div className="container flex gap-6">
                  <div className="flex flex-col p-4 gap-4 w-[60%] rounded-lg drop-shadow-md bg-white">
                    <h1 className="text-xs md:text-base">ประเมิณเกรดรายวิชา</h1>
                    <table className="table-auto border-separate border-spacing-2">
                      <thead>
                        <td className="text-xs md:text-base">วิชา</td>
                        <td className="text-xs md:text-base">เกรด</td>
                      </thead>
                      <tbody>
                        {predicts.message.map((item, index) => (
                          <tr key={index}>
                            <td>
                              {item.subject_id} {item.sub_name}
                            </td>
                            <td>{item.grade}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <div className="flex flex-col w-[40%]">
                    <div className="flex flex-col p-4 gap-4 rounded-lg drop-shadow-md bg-white">
                      <h1 className="text-xs md:text-base">
                        อาชีพที่เป็นไปได้
                      </h1>
                      <div className="flex items-center justify-center font-semibold text-xs md:text-base">
                        {career}
                      </div>
                    </div>
                    <div className="flex justify-center py-6">
                      <button
                        type="submit"
                        className="w-[80px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                      >
                        กลับ
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
      )}
    </>
  );
};

export default ResultPredict;

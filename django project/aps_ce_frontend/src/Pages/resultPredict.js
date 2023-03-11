import React, { useState } from "react";
import PredictStudent from "./predictStudent";

const ResultPredict = ({ predicts }) => {
  const [back, setBack] = useState(false);

  const career = predicts.message.at(-1);
    console.log(career);
  return (
    <>
      {back ? (
        <PredictStudent />
      ) : (
        <div>
          <h1>Result Predict:</h1>
          <form onSubmit={() => setBack(true)}>
            <ul>
              {predicts.message.map((item,index) => (
              <li key={index}>
                {item.subject_id} - {item.sub_name}: {item.grade}
              </li>
            ))}
            <li>Career: {career}</li>
            </ul>
            <button type="submit">Back to Predict</button>
          </form>
        </div>
      )}
    </>
  );
};



export default ResultPredict;
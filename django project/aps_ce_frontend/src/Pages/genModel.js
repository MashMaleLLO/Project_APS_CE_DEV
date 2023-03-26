import React from "react";
import axios from "axios";

import { useState } from "react";

const GenModel = () => {
  // let formData = new FormData();
  // const [name, setName] = useState();
  // if (name) {
  //   formData.append(name);
  // }

  const handleSubmit = (e) => {
    e.preventDefault();
    let dat = {
      "name" : e.target.first_name.value,
      "pred" : e.target.pred.value
    }
    async function fetchData() {
      let res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/getModel/` + e.target.curri.value, dat);

    }

    fetchData();
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>Create You Model</h1>
        <select name='pred'>
          <option value="Grade">Predict By Grade</option>
          <option value="Class">Predict By Class</option>
        </select>
        <select name='curri'>
          <option value="Com">วิศวกรรมคอมพิวเตอร์</option>
          <option value="Continue">วิศวกรรมคอมพิวเตอร์ (ต่อเนื่อง)</option>
        </select>
        <input id="first_name" name="first_name" type="text"/>
        <button type="submit">Submit form</button>
      </form>
    </div>
  );
};

export default GenModel;

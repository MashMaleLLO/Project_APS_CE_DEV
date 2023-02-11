import { useState, useEffect } from "react";
import React from "react";
import axios from "axios";

const baseURL = "http://localhost:8000/students";

const OutputCareer = () => {
  const [post, setPost] = useState(null);

  useEffect(() => {
    axios.get(baseURL).then((response) => {
      setPost(response.data);
    //   console.log(response.data);
    });
  });

  if (!post) return null;

  return(
    <><h1>career</h1><h1>{post.career}</h1></>
  )
};

export default OutputCareer;

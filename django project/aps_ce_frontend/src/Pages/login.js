import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';
import {createRoot} from 'react-dom/client';

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const rootElement = document.getElementById('root');
  const root = createRoot(rootElement);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/signin", {
        username,
        password,
      });
      const { data } = response;
      if (data.message) {
        localStorage.setItem("isLoggedIn", true);
        console.log('kuycaffee')
        navigate(`/`);
      } else {
        setErrorMessage(data.message);
      }
    } catch (error) {
      setErrorMessage(
        "An error occurred while trying to log in. Please try again later."
      );
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    navigate(`/`);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          <b>Username:</b>
          <input
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </label>
        <br />
        <br />
        <label>
          <b>Password:</b>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <br />
        <br />
        <button type="submit">Login</button>
        <br />
        <br />
        {errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
      </form>
      {localStorage.getItem("isLoggedIn") === "true" && (
        
        <div>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  );
};

export default Login;

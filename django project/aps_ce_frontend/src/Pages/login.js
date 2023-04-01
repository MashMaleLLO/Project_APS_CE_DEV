import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { createRoot } from "react-dom/client";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const rootElement = document.getElementById("root");
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
    <>
      <div className="flex flex-col justify-center items-center min-h-screen">
        <form onSubmit={handleSubmit}>
          <div className="container mx-auto flex items-center justify-center rounded-lg drop-shadow-md bg-white px-4 py-12 w-full md:w-[550px] ">
            <div className="flex flex-col gap-4">
              <h1 className="mb-4 font-bold text-xl md:text-3xl text-center">
                เข้าสู่ระบบ
              </h1>
              <div className="space-y-2">
                <span className="text-base md:text-lg">ชื่อผู้ใช้งาน</span>
                <input
                  type="username"
                  value={username}
                  className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                  onChange={(event) => setUsername(event.target.value)}
                />
              </div>

              <div className="space-y-2">
                <span className="text-base md:text-lg">รหัสผ่าน</span>
                <input
                  type="password"
                  value={password}
                  className="w-full px-4 py-2 bg-white border border-grey-300 rounded-lg focus:bg-grey-200 focus:border-[#FB8500] focus:outline-none"
                  onChange={(event) => setPassword(event.target.value)}
                />
                <div className="text-center py-6">
                  <button
                    type="submit"
                    className="text-white text-lg md:text-2xl px-6 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
                  >
                    เข้าสู่ระบบ
                  </button>
                </div>
              </div>
            </div>
          </div>

          {errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
        </form>
        {localStorage.getItem("isLoggedIn") === "true" && (
          <div>
            <button onClick={handleLogout}>Logout</button>
          </div>
        )}
      </div>
    </>
  );
};

export default Login;

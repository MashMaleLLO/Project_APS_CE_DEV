import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { createRoot } from "react-dom/client";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();

  const rootElement = document.getElementById("root");
  const root = createRoot(rootElement);

  const handleSubmit = async (event, type) => {
    event.preventDefault();
    if (type == "kammakan") {
      try {
        const response = await axios.post(
          `${process.env.REACT_APP_BACKEND_URL}/signin`,
          {
            username,
            password,
          }
        );
        const { data } = response;
        if (data.message) {
          localStorage.setItem("isLoggedIn", true);
          localStorage.setItem("role", "kammakan");
          navigate(`/`);
        } else {
          setErrorMessage(data.message);
        }
      } catch (error) {
        setErrorMessage(
          "An error occurred while trying to log in. Please try again later."
        );
      }
    }
    if (type == "student") {
      try {
        const response = await axios.post(
          `${process.env.REACT_APP_BACKEND_URL}/signin`,
          {
            username,
            password,
          }
        );
        const { data } = response;
        if (data.message) {
          localStorage.setItem("isLoggedIn", true);
          localStorage.setItem("role", "student");
          navigate(`/`);
        } else {
          setErrorMessage(data.message);
        }
      } catch (error) {
        setErrorMessage(
          "An error occurred while trying to log in. Please try again later."
        );
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    navigate(`/`);
  };

  const [selectedButton, setSelectedButton] = useState(true);
  const handleButtonClick = (type) => {
    setSelectedButton(type);
    setLogin(type);
  };

  console.log(selectedButton);

  return (
    <div className="w-full py-12 lg:min-h-screen">
      <div className="flex flex-col items-center justify-center py-6">
        <h1 className="mb-4 font-bold text-xl md:text-3xl text-center">
          เข้าสู่ระบบ
        </h1>
        <div className="flex items-center justify-center">
          <button
            className={`${
              selectedButton === true ? "text-black" : "text-[#A7A7A7]"
            } text-xl md:text-2xl font-bold cursor-pointer py-4 px-4`}
            onClick={() => handleButtonClick(true)}
          >
            กรรมการหลักสูตร
          </button>

          <span className="text-xl md:text-2xl">|</span>
          <button
            className={`${
              selectedButton === false ? "text-black" : "text-[#A7A7A7]"
            } text-xl md:text-2xl font-bold cursor-pointer py-4 px-4`}
            onClick={() => handleButtonClick(false)}
          >
            นักศึกษา
          </button>
        </div>
      </div>
      {login ? (
        <div className="flex flex-col justify-center items-center">
          <form onSubmit={(event) => handleSubmit(event, "kammakan")}>
            <div className="container mx-auto flex items-center justify-center rounded-lg drop-shadow-md bg-white px-4 py-12 w-full md:w-[550px]">
              <div className="flex flex-col gap-4">
                {/* <h1>กรรมการหลักสูตร</h1> */}
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
                      className="text-white text-lg md:text-xl px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
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
      ) : (
        <div className="flex flex-col justify-center items-center">
          <form onSubmit={(event) => handleSubmit(event, "student")}>
            <div className="container mx-auto flex items-center justify-center rounded-lg drop-shadow-md bg-white px-4 py-12 w-full md:w-[550px]">
              <div className="flex flex-col gap-4">
                {/* <h1>นักศึกษา</h1> */}
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
                      className="text-white text-lg md:text-xl px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204]"
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
      )}
    </div>
  );
};

export default Login;

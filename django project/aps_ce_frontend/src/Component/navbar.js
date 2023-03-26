import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  let navigate = useNavigate();
  const homePage = () => {
    let homePage = ``;
    navigate(homePage);
  };
  const outputCareer = () => {
    let outputCareer = `outputCareer`;
    navigate(outputCareer);
  };
  const predictStudent = () => {
    let predictStudent = `predictStudent`;
    navigate(predictStudent);
  };
  const recommendSubject = () => {
    let recommendSubject = `recommendSubject`;
    navigate(recommendSubject);
  };
  const login = () => {
    let login = `login`;
    navigate(login);
  };
  const dataUpload = () => {
    let dataUpload = `dataUpload`;
    navigate(dataUpload);
  };

  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  const role = localStorage.getItem("role") === "kammakan";

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      localStorage.removeItem("isLoggedIn");
      navigate(`/`);
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Button
            variant="h1"
            component="div"
            sx={{ flexGrow: 1 }}
            onClick={homePage}
          >
            หน้าหลัก
          </Button>
          <Button
            variant="h1"
            component="div"
            sx={{ flexGrow: 1 }}
            onClick={outputCareer}
          >
            สายงานบัณฑิต
          </Button>
          <Button
            variant="h1"
            component="div"
            sx={{ flexGrow: 1 }}
            onClick={predictStudent}
          >
            พยากรณ์นักศึกษา
          </Button>
          <Button
            variant="h1"
            component="div"
            sx={{ flexGrow: 1 }}
            onClick={recommendSubject}
          >
            แนะนำวิชาเลือก
          </Button>
          {isLoggedIn && role && (
            <Button
              variant="h1"
              component="div"
              sx={{ flexGrow: 1 }}
              onClick={dataUpload}
            >
              อัพโหลดไฟล์
            </Button>
          ) } 
          {isLoggedIn && !role && (
            <Button
              variant="h1"
              component="div"
              sx={{ flexGrow: 1 }}
              onClick={dataUpload}
            >
              นักศึกษา
            </Button>
          ) } 
          {isLoggedIn ? (
            <Button
              variant="h1"
              component="div"
              sx={{ flexGrow: 1 }}
              onClick={handleLogout}
            >
              ออกจากระบบ
            </Button>
          ) : (
            <Button
              variant="h1"
              component="div"
              sx={{ flexGrow: 1 }}
              onClick={login}
            >
              เข้าสู่ระบบ
            </Button>
          )}
        </Toolbar>
      </AppBar>
    </Box>
  );
}

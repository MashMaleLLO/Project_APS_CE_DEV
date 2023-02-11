import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Routes, Route, useNavigate } from "react-router-dom";

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
          <Button variant="h1" component="div" sx={{ flexGrow: 1 }}>
            แนะนำวิชาเลือก
          </Button>
          <Button variant="h1" component="div" sx={{ flexGrow: 5 }}>
            เข้าสู่ระบบ
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

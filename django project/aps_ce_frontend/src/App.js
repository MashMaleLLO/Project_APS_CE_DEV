import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DataUpload from "./Pages/dataUpload";
import GenModel from "./Pages/genModel";
import ModelList from "./Pages/modelList";
import CareerUpdate from "./Pages/updateStudentCareer";
import OutputCareer from "./Pages/outputCareer";
import PredictStudent from "./Pages/predictStudent";
import HomePage from "./Pages/index";
import Login from "./Pages/login";
import RecommendSubject from "./Pages/recommendSubject";
import Navbar from "./Component/navbar";
import Footer from "./Component/footer";
import { theme } from "./Component/theme";
import { ThemeProvider } from "@mui/material/styles";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/outputCareer" element={<OutputCareer />} />
          <Route path="/predictStudent" element={<PredictStudent />} />
          <Route path="/recommendSubject" element={<RecommendSubject />} />
          <Route path="/login" element={<Login />} />

          <Route
            path="/dataUpload"
            element={
              <center>
                <DataUpload />
              </center>
            }
          />
          <Route
            path="/genModel"
            element={
              <center>
                <GenModel />
              </center>
            }
          />
          <Route
            path="/temp"
            element={
              <center>
                <ModelList />
              </center>
            }
          />
          <Route
            path="/careerUpdate"
            element={
              <center>
                <CareerUpdate />
              </center>
            }
          />
        </Routes>
      </div>
      <Footer />
    </ThemeProvider>
  );
}

export default App;
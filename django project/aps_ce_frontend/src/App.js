import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { theme } from "./Component/theme";
import { ThemeProvider } from "@mui/material/styles";
import Navbar from "./Component/navbar";
import Footer from "./Component/footer";
import HomePage from "./Pages/index";
import Login from "./Pages/login";
import OutputCareer from "./Pages/outputCareer";
import PredictStudent from "./Pages/predictStudent";
import RecommendSubject from "./Pages/recommendSubject";
import DataUpload from "./Pages/dataUpload";
import DataEdit from "./Pages/dataEdit";
import GenModel from "./Pages/genModel";
import ModelList from "./Pages/modelList";
import CareerUpdate from "./Pages/updateStudentCareer";
import Student from "./Pages/student";
import Upload from "./Pages/Upload"
import Test2 from "./Pages/Test2"


function App() {
  return (
    <ThemeProvider theme={theme}>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/outputCareer" element={<OutputCareer />} />
          <Route path="/predictStudent" element={<PredictStudent />} />
          <Route path="/recommendSubject" element={<RecommendSubject />} />
          <Route path="/dataUpload" element={<DataUpload />} />
          <Route path="/dataEdit/:id" element={<DataEdit />} />
          <Route path="/genModel" element={<GenModel />} />
          <Route path="/temp" element={<ModelList />} />
          <Route path="/careerUpdate" element={<CareerUpdate />} />
          <Route path="/Upload" element={<Upload />} />
          <Route path="/Student" element={<Student />} />
          <Route path="/Test2" element={<Test2 />} />
        </Routes>
      </div>
      <Footer />
    </ThemeProvider>
  );
}

export default App;

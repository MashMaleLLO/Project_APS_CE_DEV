import React from 'react';
import { Routes, Route } from 'react-router-dom';

import SubjectUpload from './Pages/subjectUpload';
import ReqAna from './Pages/reqAna';
import GenModel from './Pages/genModel';
import ModelList from './Pages/modelList';
import CareerUpdate from './Pages/updateStudentCareer';

import OutputCareer from './Pages/outputCareer';
import PredictStudent from './Pages/predictStudent';
import HomePage from './Pages/index'
import Login from './Pages/login'
import RecommendSubject from './Pages/recommendSubject'

import Navbar from './Component/navbar';
import Footer from './Component/footer';
import { theme } from './Component/theme';
import { ThemeProvider } from '@mui/material/styles';

function App() {
    return (
        <ThemeProvider theme={theme}>
        <Navbar/>
        <Routes>

            <Route path="/" element={<center><HomePage/></center>} />
            <Route path="/outputCareer" element={<center><OutputCareer/></center>} />
            <Route path="/predictStudent" element={<center><PredictStudent/></center>} />
            <Route path="/recommendSubject" element={<center><RecommendSubject/></center>} />
            <Route path="/login" element={<center><Login/></center>} />


            <Route path="/subjectUpload" element={<center><SubjectUpload/></center>} />
            <Route path="/reqAna" element={<center><ReqAna/></center>} />
            <Route path="/genModel" element={<center><GenModel/></center>} />
            <Route path="/temp" element={<center><ModelList/></center>} />
            <Route path="/careerUpdate" element={<center><CareerUpdate/></center>} />
            
        </Routes>
        <Footer/>
        </ThemeProvider>
    );
}

export default App;
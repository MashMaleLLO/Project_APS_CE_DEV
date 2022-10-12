import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './Pages/index'
import SubjectUpload from './Pages/subjectUpload';
import ReqAna from './Pages/reqAna';

function App() {
    return (
        <>
        <Routes>
            <Route path="/" element={<center><HomePage/></center>} />
            <Route path="/subjectUpload" element={<center><SubjectUpload/></center>} />
            <Route path="/reqAna" element={<center><ReqAna/></center>} />
        </Routes>
        </>
    );
}

export default App;
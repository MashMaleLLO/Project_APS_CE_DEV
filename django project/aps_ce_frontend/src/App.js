import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './Pages/index'
import SubjectUpload from './Pages/subjectUpload';

function App() {
    return (
        <>
        <Routes>
            <Route path="/" element={<center><HomePage/></center>} />
            <Route path="/subjectUpload" element={<center><SubjectUpload/></center>} />
        </Routes>
        </>
    );
}

export default App;
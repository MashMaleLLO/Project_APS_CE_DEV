import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './Pages/index'

function App() {
    return (
        <>
        <Routes>
            <Route path="/" element={<center><HomePage/></center>} />
        </Routes>
        </>
    );
}

export default App;
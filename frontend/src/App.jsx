import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import ConferenceInfo from "./pages/Fickett_ConferenceInfo";
import PaperPage from "./pages/Paper";

function App() {
  return (
    <Router>
      <div className="App">
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/conference-info" element={<ConferenceInfo />} />
            <Route path="/papers" element={<PaperPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

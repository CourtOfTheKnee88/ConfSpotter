import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./Login";
import SignUp from "./SignUp";
import Dashboard from "./Dashboard";
import ConferenceInfo from "./ConferenceInfo";

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
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

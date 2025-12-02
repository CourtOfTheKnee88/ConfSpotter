import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  function goToConferenceInfo() {
    navigate("/conference-info");
  }

  function goToDashboard() {
    navigate("/dashboard");
  }

  function goToSignUp() {
    navigate("/sign-up");
  }

  return (
    <div className="bg-blue-200 h-screen flex items-center justify-center flex-col gap-10">
      <div className="space-x-3">
        <button
          onClick={goToConferenceInfo}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Conference Info Page
        </button>
        <button
          onClick={goToDashboard}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Dashboard Page
        </button>
        <button
          onClick={goToSignUp}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Sign Up Page
        </button>
      </div>
      <div className="bg-white rounded-xl py-10 px-20 shadow-lg flex flex-col gap-10">
        <h1 className="font-bold text-4xl text-center">Confrence Spotter</h1>

        <div>
          <h1>Login</h1>
          <div>
            <p>Email:</p>
          </div>
          <div>
            <p>Password:</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

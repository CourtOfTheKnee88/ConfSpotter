import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  function goToConferenceInfo() {
    navigate("/conference-info");
  }

  function goToDashboard() {
    navigate("/dashboard");
  }

  function goToSignUp() {
    navigate("/sign-up");
  }

  function handleLogin(username, password) {
    // call the api to verify login credentials
    // if successful, navigate to dashboard
    navigate("/dashboard");
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

        <form className="flex flex-col gap-6">
          <input
            type="email"
            placeholder="Email"
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            type="password"
            placeholder="Password"
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            onPress={handleLogin(username, password)}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;

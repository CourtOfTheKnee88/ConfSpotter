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

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const response = await fetch("/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Success:", data.message);
        setUsername("");
        setPassword("");
        goToDashboard();
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
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

        <form onSubmit={handleLogin} className="flex flex-col gap-6">
          <input
            type="email"
            placeholder="Email"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
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

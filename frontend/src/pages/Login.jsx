import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function goToDashboard() {
    navigate("/dashboard");
  }

  function goToSignUp() {
    navigate("/sign-up");
  }

  async function handleLogin(e) {
    e.preventDefault();
    setError("");

    if (!login || !password) {
      setError("Please enter both username/email and password");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:5001/api/users/verify-login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login,
            password_hash: password,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        console.log("Success:", data.message);
        // Store user info in localStorage if needed
        localStorage.setItem("user", JSON.stringify(data.user));
        setLogin("");
        setPassword("");
        goToDashboard();
      } else {
        setError(data.message || "Invalid credentials. Please try again.");
      }
    } catch (error) {
      console.error("Network error:", error);
      setError("Unable to connect to server. Please try again later.");
    }
  }

  return (
    <div className="bg-blue-200 h-screen flex items-center justify-center flex-col gap-10">
      <div className="bg-white rounded-xl py-10 px-20 shadow-lg flex flex-col">
        <h1 className="font-bold text-4xl text-center pb-10">
          Confrence Spotter
        </h1>

        <form onSubmit={handleLogin} className="flex flex-col gap-6">
          <input
            type="text"
            placeholder="Username or Email"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Login
          </button>
        </form>
        <button
          onClick={goToSignUp}
          className="text-blue-500 hover:text-blue-600 underline pt-3"
        >
          Don't have an account? Sign Up
        </button>
      </div>
    </div>
  );
};

export default Login;

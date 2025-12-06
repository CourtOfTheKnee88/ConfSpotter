import React, { useState } from "react";
import axios from "axios";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [interest1, setInterest1] = useState("");
  const [interest2, setInterest2] = useState("");
  const [interest3, setInterest3] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/api/users", {
        username: username,
        email: email,
        password_hash: password,
      });

      setSuccess("Account created successfully!");
      setUsername("");
      setEmail("");
      setPhone("");
      setPassword("");
      setConfirmPassword("");
      setInterest1("");
      setInterest2("");
      setInterest3("");
    } catch (err) {
      if (err.response?.data?.message) {
        setError(err.response.data.message);
      } else {
        setError("Server error — please try again later.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
      <div style={{ textAlign: 'center', width: '100%', maxWidth: 420, padding: 16 }}>
        <h2>Signup</h2>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>{success}</p>}

        <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, marginTop: 8 }}>
          <input
            type="username"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />
          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />
          <input
            type="phone"
            placeholder="Enter phone number (optional)"
            value={email}
            onChange={(e) => setPhone(e.target.value)}
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />

          <input
            type="password"
            placeholder="Enter confirm password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />

          <input
            type="interest 1"
            placeholder="Enter interest 1"
            value={interest1}
            onChange={(e) => setInterest1(e.target.value)}
            required
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />
          <input
            type="interest 2"
            placeholder="Enter interest 2 (optional)"
            value={interest2}
            onChange={(e) => setInterest2(e.target.value)}
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />
          <input
            type="interest 3"
            placeholder="Enter interest 3 (optional)"
            value={interest3}
            onChange={(e) => setInterest3(e.target.value)}
            style={{ width: '100%', padding: 10, boxSizing: 'border-box' }}
          />

          <button
            type="submit"
            disabled={loading}
            style={{ color: 'white', backgroundColor: loading ? '#ccc' : '#007bff', border: 'none', padding: '10px 16px', cursor: loading ? 'not-allowed' : 'pointer', borderRadius: 4, width: '100%' }}
          >
            {loading ? "Creating account..." : "Signup"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signup;


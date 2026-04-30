import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Auth.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const loginUser = async () => {
    try {
      const res = await fetch(
        `https://your-backend-url.onrender.com/login/${email}/${password}`
      );

      const data = await res.json();

      if (data && data.status === "Success") {
        navigate("/dashboard"); // redirect works
      } else {
        alert("Invalid Login");
      }
    } catch (error) {
      console.error(error);
      alert("Backend not reachable");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>🌿 Smart Irrigation</h1>
        <h2>Login</h2>

        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={loginUser}>Login</button>

        <p>
          New user? <Link to="/signup">Create Account</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
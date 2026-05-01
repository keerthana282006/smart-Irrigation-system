import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Auth.css";

const API_URL = "http://localhost:5000";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const loginUser = async () => {
    // ✅ validation
    if (!email.trim() || !password.trim()) {
      alert("Please enter email and password");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email.trim().toLowerCase(), // ✅ match signup format
          password: password.trim(),
        }),
      });

      // ✅ handle invalid JSON safely
      let data;
      try {
        data = await res.json();
      } catch {
        throw new Error("Invalid server response");
      }

      console.log("Login Response:", data);

      if (res.ok && data.status === "success") {
        alert("Login Successful");

        // ✅ store user info (optional but useful)
        localStorage.setItem("user", JSON.stringify(data.user));

        navigate("/dashboard");
      } else {
        alert(data.message || "Invalid credentials");
      }

    } catch (error) {
      console.error("Login Error:", error);
      alert("Backend not reachable or server error");
    } finally {
      setLoading(false);
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
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={loginUser} disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        <p>
          New user? <Link to="/signup">Create Account</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Auth.css";

const API_URL = "http://localhost:5000";

function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const signupUser = async () => {
    // ✅ validation
    if (!name.trim() || !email.trim() || !password.trim()) {
      alert("All fields are required");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name.trim(),
          email: email.trim().toLowerCase(), // ✅ avoid duplicate case issue
          password: password.trim(),
        }),
      });

      // ✅ handle non-JSON or server crash
      let data;
      try {
        data = await res.json();
      } catch {
        throw new Error("Invalid server response");
      }

      console.log("Signup Response:", data);

      if (res.ok && data.status === "success") {
        alert("Signup Successful");
        navigate("/"); // go to login
      } else {
        alert(data.message || "Signup failed");
      }

    } catch (err) {
      console.error("Signup Error:", err);
      alert("Backend not reachable or server error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>🌿 Smart Irrigation</h1>
        <h2>Signup</h2>

        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

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

        <button onClick={signupUser} disabled={loading}>
          {loading ? "Creating..." : "Create Account"}
        </button>

        <p>
          Already have account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
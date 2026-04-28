import React, { useEffect, useState } from "react";

function WaterEfficiency() {

  const [wue, setWue] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://smart-irrigation-system-3-ny8u.onrender.com/WaterEfficiency")
      .then((res) => res.json())
      .then((data) => {
        setWue(data.water_use_efficiency);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div
      className="container d-flex justify-content-center align-items-center"
      style={{ minHeight: "100vh" }}
    >

      <div
        className="card shadow-lg p-4 text-center"
        style={{
          width: "500px",
          borderRadius: "15px"
        }}
      >

        <h2 className="text-primary mb-3">
          💦 Water Efficiency Module
        </h2>

        <p className="text-muted">
          Water Use Efficiency Result
        </p>

        {loading ? (
          <h4>Loading...</h4>
        ) : (
          <h1 className="text-success mb-4">
            {wue}
          </h1>
        )}

        <img
          src="http://127.0.0.1:5000/static/project_table.png"
          alt="table"
          style={{
            width: "100%",
            height: "220px",
            objectFit: "contain",
            borderRadius: "10px"
          }}
        />

      </div>

    </div>
  );
}

export default WaterEfficiency;
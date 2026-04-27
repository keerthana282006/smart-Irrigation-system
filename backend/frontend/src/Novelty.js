import React, { useEffect, useState } from "react";

function Novelty() {

  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/novelty")
      .then((res) => res.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  if (!data) {
    return (
      <div className="container mt-5">
        <h2>Loading Novelty Module...</h2>
      </div>
    );
  }

  return (
    <div className="container mt-5">

      <h1>🚀 Novelty Module</h1>

      <div className="card p-4 shadow mt-4">

        <h3>🌱 Irrigation Decision</h3>
        <p>{data.decision}</p>

        <h3>💧 Water Saved</h3>
        <p>{data.water_saved}</p>

        <h3>🌾 Crop Yield</h3>
        <p>{data.yield}</p>

        <h3>📊 Water Use Efficiency</h3>
        <p>{data.wue}</p>

        <h3>🍀 Crop Health</h3>
        <p>{data.crop_health}</p>

      </div>

    </div>
  );
}

export default Novelty;
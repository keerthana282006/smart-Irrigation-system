import React, { useEffect, useState } from "react";
import axios from "axios";

function TTN() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/data")
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, []);

  if (!data) {
    return <h3>Loading TTN...</h3>;
  }

  return (
    <div className="container mt-5">
      <h2>📡 TTN Sensor Module</h2>

      <p>Soil Moisture: {data.ttn?.soil_moisture || "--"} %</p>
      <p>Temperature: {data.ttn?.temperature || "--"} °C</p>
    </div>
  );
}

export default TTN;
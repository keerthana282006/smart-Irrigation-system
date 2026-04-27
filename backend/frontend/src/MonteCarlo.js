import React, { useState } from "react";

function MonteCarlo() {

  const [result, setResult] = useState("");

  function runSimulation() {

    let moisture = Math.floor(Math.random() * 100);
    let rainfall = Math.floor(Math.random() * 20);

    if (moisture < 40 && rainfall < 5) {
      setResult("Irrigation Required");
    } else {
      setResult("No Irrigation Needed");
    }
  }

  return (
    <div className="container mt-5">

      <div className="card shadow p-4">

        <h2 className="text-danger">
          📊 Monte Carlo Simulation
        </h2>

        <p className="mt-3">
          Random prediction based on soil moisture and rainfall.
        </p>

        <button
          className="btn btn-primary mt-3"
          onClick={runSimulation}
        >
          Run Simulation
        </button>

        {result && (
          <h3 className="mt-4 text-success">
            {result}
          </h3>
        )}

        <img
          src="http://127.0.0.1:5000/static/live_graph.png"
          alt="graph"
          className="img-fluid mt-4 rounded"
        />

      </div>

    </div>
  );
}

export default MonteCarlo;
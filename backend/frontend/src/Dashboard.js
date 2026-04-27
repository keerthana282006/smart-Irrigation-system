import React from "react";
import { Link } from "react-router-dom";
import "./App.css";

function Dashboard() {

return (

<div>

<div className="header">
<h1>Smart Irrigation Dashboard</h1>
</div>

<div className="card-grid">

<Link to="/prediction" className="card">
Prediction Panel
</Link>

<Link to="/weather" className="card">
Weather Module
</Link>

<Link to="/ttn" className="card">
TTN Module
</Link>

<Link to="/hydraulic" className="card">
Hydraulic Module
</Link>

<Link to="/irriframe" className="card">
Irriframe Module
</Link>

<Link to="/decision" className="card">
Decision Module
</Link>

<Link to="/water" className="card">
Water Efficiency
</Link>

<Link to="/monte" className="card">
Monte Carlo
</Link>

<Link to="/graph" className="card">
Live Graph
</Link>

<Link to="/novelty" className="card">
Novelty Module
</Link>

</div>

</div>

)

}

export default Dashboard;
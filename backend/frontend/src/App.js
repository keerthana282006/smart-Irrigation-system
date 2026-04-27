import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./Login";
import Signup from "./Signup";
import Dashboard from "./Dashboard";
import Prediction from "./Prediction";

import Weather from "./Weather";
import TTN from "./TTN";
import Hydraulic from "./Hydraulic";
import Irriframe from "./Irriframe";
import Decision from "./Decision";
import WaterEfficiency from "./WaterEfficiency";
import MonteCarlo from "./MonteCarlo";
import LiveGraph from "./LiveGraph";
import Novelty from "./Novelty";

function App() {

return (

<Router>

<Routes>

<Route path="/" element={<Login/>}/>
<Route path="/signup" element={<Signup/>}/>
<Route path="/dashboard" element={<Dashboard/>}/>
<Route path="/prediction" element={<Prediction/>}/>
<Route path="/graph" element={<LiveGraph/>}/>
<Route path="/novelty" element={<Novelty/>}/>

<Route path="/weather" element={<Weather/>}/>
<Route path="/ttn" element={<TTN/>}/>
<Route path="/hydraulic" element={<Hydraulic/>}/>
<Route path="/irriframe" element={<Irriframe/>}/>
<Route path="/decision" element={<Decision/>}/>
<Route path="/water" element={<WaterEfficiency/>}/>
<Route path="/monte" element={<MonteCarlo/>}/>

</Routes>

</Router>

)

}

export default App;
import React, { useState } from "react";
import "./App.css";

function Prediction(){

const [soil,setSoil] = useState("")
const [rain,setRain] = useState("")
const [flow,setFlow] = useState("")

const [decision,setDecision] = useState("")
const [wue,setWue] = useState("")

const predict = () => {

let irrigation = "No Irrigation Required"

if(soil < 40 && rain < 5){
irrigation = "Irrigation Required"
}

setDecision(irrigation)

// Water Use Efficiency
let yield_value = 2500

let efficiency = yield_value / (Number(flow) + Number(rain) + 1)

setWue(efficiency.toFixed(2))

}

return(

<div className="prediction">

<h1>User Input Prediction Panel</h1>

<div className="input-grid">

<input
placeholder="Soil Moisture (%)"
onChange={(e)=>setSoil(e.target.value)}
/>

<input
placeholder="Temperature (°C)"
onChange={(e)=>setTemp(e.target.value)}
/>

<input
placeholder="Rainfall (mm)"
onChange={(e)=>setRain(e.target.value)}
/>

<input
placeholder="Flow Rate"
onChange={(e)=>setFlow(e.target.value)}
/>

</div>

<button onClick={predict}>
Predict Decision
</button>

<div className="result">

<h2>Decision : {decision}</h2>
<h2>Water Efficiency : {wue}</h2>

</div>

</div>

)

}

export default Prediction;
import React,{useState} from "react";

function Decision(){

const [soil,setSoil]=useState("")
const [temp, setTemp] = useState("");
const [result,setResult]=useState("")

const decide=()=>{

if(soil < 40){
setResult("Irrigation Required")
}
else{
setResult("No Irrigation Needed")
}

}

return(

<div>

<h1>Irrigation Decision</h1>

<input
placeholder="Soil Moisture"
onChange={(e)=>setSoil(e.target.value)}
/>

<input
placeholder="Temperature"
onChange={(e)=>setTemp(e.target.value)}
/>

<button onClick={decide}>
Get Decision
</button>

<h2>{result}</h2>

</div>

)

}

export default Decision;
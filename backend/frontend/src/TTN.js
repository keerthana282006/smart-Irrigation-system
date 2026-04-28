import React,{useEffect,useState} from "react"
import axios from "axios"

function TTN(){

const [data,setData] = useState({})

useEffect(()=>{

axios.get("https://smart-irrigation-system-3-ny8u.onrender.com/TTN")
.then(res=>setData(res.data))

},[])

return(

<div className="container mt-5">

<h2>📡 TTN Sensor</h2>

<p>Soil Moisture : {data?.ttn?.soil_moisture}</p>
<p>Temperature : {data?.ttn?.temperature}</p>

</div>

)

}

export default TTN;
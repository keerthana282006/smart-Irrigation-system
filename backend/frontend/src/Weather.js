import React, {useEffect,useState} from "react"
import axios from "axios"

function Weather(){

const [data,setData] = useState(null)

useEffect(()=>{

axios.get("http://127.0.0.1:5000/data")
.then(res=>setData(res.data))
.catch(err=>console.log(err))

},[])

if(!data){
return <h3>Loading Weather...</h3>
}

return(

<div className="container mt-5">

<h2>🌤 Weather Module</h2>

<p>Temperature : {data.weather?.temperature || "--"} °C</p>
<p>Wind : {data.weather?.wind || "--"} km/h</p>

</div>

)

}

export default Weather;
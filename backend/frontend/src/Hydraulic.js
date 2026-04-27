import React,{useEffect,useState} from "react"
import axios from "axios"

function Hydraulic(){

const [data,setData] = useState(null)

useEffect(()=>{

axios.get("http://127.0.0.1:5000/data")
.then(res=>setData(res.data))
.catch(err=>console.log(err))

},[])

if(!data){
return <h3>Loading Hydraulic...</h3>
}

return(

<div className="container mt-5">

<h2>💧 Hydraulic</h2>

<p>Pressure : {data.flow?.pressure || "--"}</p>
<p>Flow Rate : {data.flow?.flow_rate || "--"}</p>

</div>

)

}

export default Hydraulic;
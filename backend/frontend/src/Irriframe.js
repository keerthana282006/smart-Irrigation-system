import React,{useEffect,useState} from "react"
import axios from "axios"

function Irriframe(){

const [data,setData] = useState({})

useEffect(()=>{

axios.get("https://smart-irrigation-system-3-ny8u.onrender.com")
.then(res=>setData(res.data))

},[])

return(

<div className="container mt-5">

<h2>🌿 Irriframe</h2>

<p>Water Required : {data?.irriframe?.water}</p>
<p>Duration : {data?.irriframe?.duration}</p>

</div>

)

}

export default Irriframe;
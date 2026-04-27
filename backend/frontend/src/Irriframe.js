import React,{useEffect,useState} from "react"
import axios from "axios"

function Irriframe(){

const [data,setData] = useState({})

useEffect(()=>{

axios.get("http://127.0.0.1:5000/data")
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
import React,{useEffect,useState} from "react"
import axios from "axios"

function LiveGraph(){

const [img,setImg] = useState("")

useEffect(()=>{

fetchGraph()

const interval = setInterval(()=>{
fetchGraph()
},5000)

return ()=>clearInterval(interval)

},[])

const fetchGraph = ()=>{

axios.get("https://smart-irrigation-system-3-ny8u.onrender.com/static/graph")
.then(res=>{

setImg(res.data.graph + "?t=" + new Date().getTime())

})

}

return(

<div className="container mt-5">

<h2>Live Irrigation Graph</h2>

<img 
src={img}
alt="Live Graph"
style={{width:"100%"}}
/>

</div>

)

}

export default LiveGraph
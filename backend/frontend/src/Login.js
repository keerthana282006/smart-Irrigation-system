import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Login(){

const navigate = useNavigate();

const [role,setRole] = useState("user")
const [username,setUsername] = useState("")
const [password,setPassword] = useState("")

const handleLogin = (e) => {

e.preventDefault()

const savedUser = JSON.parse(localStorage.getItem("user"))

if(!savedUser){
alert("Please create account first")
return
}

if(
username === savedUser.username &&
password === savedUser.password &&
role === savedUser.role
){
navigate("/dashboard")
}
else{
alert("Invalid Credentials")
}

}

return(

<div className="login-container">

<div className="login-box">

<h1>Smart Irrigation Login</h1>

<form onSubmit={handleLogin}>

<select
value={role}
onChange={(e)=>setRole(e.target.value)}
>

<option value="user">User</option>
<option value="admin">Admin</option>

</select>

<input
type="text"
placeholder="Username"
value={username}
onChange={(e)=>setUsername(e.target.value)}
required
/>

<input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
required
/>

<button type="submit">
Login
</button>

</form>

<p>

Don't have account ?

<button onClick={()=>navigate("/signup")}>
Sign Up
</button>

</p>

</div>

</div>

)

}

export default Login;
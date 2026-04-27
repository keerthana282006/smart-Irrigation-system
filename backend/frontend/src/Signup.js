import React,{useState} from "react";
import {useNavigate} from "react-router-dom";
import "./App.css";

function Signup(){

const navigate = useNavigate()

const [role,setRole] = useState("user")
const [username,setUsername] = useState("")
const [email,setEmail] = useState("")
const [password,setPassword] = useState("")
const [confirm,setConfirm] = useState("")

const handleSignup = (e) => {

e.preventDefault()

if(username.length < 3){
alert("Username must be 3 characters")
return
}

if(!email.includes("@")){
alert("Invalid Email")
return
}

if(password.length < 5){
alert("Password must be 5 characters")
return
}

if(password !== confirm){
alert("Password not matching")
return
}

const user = {
role,
username,
email,
password
}

localStorage.setItem("user",JSON.stringify(user))

alert("Account Created Successfully")

navigate("/")

}

return(

<div className="login-container">

<div className="login-box">

<h1>Create Account</h1>

<form onSubmit={handleSignup}>

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
type="email"
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
required
/>

<input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
required
/>

<input
type="password"
placeholder="Confirm Password"
value={confirm}
onChange={(e)=>setConfirm(e.target.value)}
required
/>

<button type="submit">
Create Account
</button>

</form>

</div>

</div>

)

}

export default Signup;
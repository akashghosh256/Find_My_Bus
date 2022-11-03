function validate(){
var username=document.getElementById("username").value;
var password=document.getElementById("password").value;
if ( username == "user" && password == "user"){
alert ("Login successfully");
//window.location = "success.html"; // Redirecting to other page.
return false;
}
else{
alert("Wrong username or password");
}}

function sendMail(){
 var params ={
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    location: document.getElementById("location").value,
    date: document.getElementById("date").value,
    description: document.getElementById("description").value,
 };

const serviceID="service_wzfvzxe";
const templateID = "template_4v3dsxn";

 emailjs.send(serviceID, templateID, params)
    .then(res=>{
        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        location: document.getElementById("location").value="";
        date: document.getElementById("date").value="";
        description: document.getElementById("description").value="";
        console.log(res);
    })
    .catch(err=>console.log(err));
}


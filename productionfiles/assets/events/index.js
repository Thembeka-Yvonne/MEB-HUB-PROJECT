
function sendMail(){
    event.preventDefault();  // Prevent form submission to avoid page reload

    const email = document.getElementById("email").value;
    if (!validateEmail(email)) {
        alert('Please enter a valid email address before submitting.');
        return;  // Stop the function if the email is not valid
    }
 var params ={
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    location: document.getElementById("location").value,
    date: document.getElementById("date").value,
    description: document.getElementById("description").value,
    time: document.getElementById("time").value,
    reply_to: document.getElementById("email").value
    };

    console.log("Sending email with params:", params);

 const serviceID="service_wzfvzxe";
 const templateID = "template_4v3dsxn";

 emailjs.send(serviceID, templateID, params)
    .then(res=>{
     console.log("Email sent successfully", res);
        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("location").value="";
        document.getElementById("date").value="";
        document.getElementById("description").value="";
        document.getElementById("time").value="";
        console.log(res);
    })
    .catch(err => {
            console.log("Error occurred: ", err);
            alert('There was an error sending the email. Please try again.');
    });
}


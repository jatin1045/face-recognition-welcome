console.log('2'+2-'2');
particlesJS.load('background', 'particles.json', function() {
    console.log('Particles.js loaded');
});

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        document.getElementById('camera-preview').srcObject = stream;
    })
    .catch(err => console.error("Camera access denied:", err));

const hour = new Date().getHours();
let greetingText = "Welcome!";
if (hour < 12) greetingText = "Good Morning!";
else if (hour < 18) greetingText = "Good Afternoon!";
else greetingText = "Good Evening!";

document.getElementById("greeting").innerText = greetingText;

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
}

document.getElementById("total-users").innerText = 150; 
document.getElementById("attendance-count").innerText = 75; 
document.getElementById("system-uptime").innerText = "15 hrs";

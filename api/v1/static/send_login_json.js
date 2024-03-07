// This script will fetch login data and send it in json format
document.getElementById('login').addEventListener('submit', function() {
event.preventDefault();

// serialize form data
const formData = new FormData(this);
const jsonData = {};
formData.forEach((value, key) => {
jsonData[key] = value;
});

// send data to server
fetch('/api/v1/practitioner/login', {
    method: 'POST',
headers: {
'content-type': 'application/json'
},
body: JSON.stringify(jsonData)
})
.then(response => {
return response.json();
}
throw new Error('Invalid login');
})


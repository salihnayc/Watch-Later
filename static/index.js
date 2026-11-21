const table = document.querySelector("#videoTableBody")
const form = document.querySelector("#addVideoForm")
const result = document.querySelector("#formResult")

form.addEventListener("submit", event => {
    event.preventDefault();
    const formData = new FormData(form);
    
    fetch("/api/add", {method: "POST", body: formData})
        .then(response => response.text())
        .then(data => result.innerHTML = data)
        .catch(error => console.error('Error:', error));
})

fetch("/api/list")
    .then(response => response.json())
    .then(data => {
        data.forEach(d => {
            table.innerHTML += `<tr><td>${d.thumbnail}</td><td>${d.title}</td><td>${d.channel}</td><td>${d.description}</td><td>${d.duration}</td></tr>`
        });
    })
    .catch(error => console.error('Error:', error));
const table = document.querySelector("#videoTableBody")
const form = document.querySelector("#addVideoForm")

form.addEventListener("submit", event => {
    event.preventDefault();
    const formData = new FormData(form);
    
    fetch("/api/add", {method: "POST", body: formData})
        .then(response => response.json())
        .then(data => {
            list()
        })
        .catch(error => {console.error('Error:', error)});
})

function list() {
    table.innerHTML = ""
    fetch("/api/list")
        .then(response => response.json())
        .then(data => {
            data.forEach(d => {
                table.innerHTML += `<tr><td>${d.thumbnail}</td><td>${d.title}</td><td>${d.channel}</td><td>${d.description}</td><td>${d.duration}</td></tr>`
            });
        })
        .catch(error => console.error('Error:', error));
}

list()
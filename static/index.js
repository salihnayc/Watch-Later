const table = document.querySelector("#videoTableBody")
const form = document.querySelector("#addVideoForm")
const formError = document.querySelector("#formError")

form.addEventListener("submit", event => {
    event.preventDefault();
    const formData = new FormData(form);
    
    fetch("/api/add", {method: "POST", body: formData})
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error.message);
            }
            else {
                formError.innerHTML = ""
                list();
            }
        })
        .catch(error => formError.innerHTML = error);
})

function list() {
    table.innerHTML = ""
    fetch("/api/list")
        .then(response => response.json())
        .then(data => {
            data.forEach(d => {
                table.innerHTML += `<tr><td>${d.videoTitle}</td><td>${d.channelTitle}</td><td>${d.videoDescription}</td><td>${d.duration}</td><td><a href="https://youtu.be/${d.videoId}">Video</a></td><td><a href="https://www.youtube.com/${d.customUrl}">Channel</a></td></tr>`
            });
        })
        .catch(error => console.error('Error:', error));
}

list()
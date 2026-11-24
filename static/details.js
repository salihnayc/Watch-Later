main = document.querySelector("main")

id = document.URL.split("/").slice(-1);

fetch(`/api/video/${id}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error.message);
        }
        main.innerHTML = data.videoTitle;
    })
    .catch(error => main.innerHTML = error)
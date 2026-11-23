const cardHolder = document.querySelector("#card-holder")
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
    cardHolder.innerHTML = ""
    fetch("/api/list")
        .then(response => response.json())
        .then(data => {
            cardHolder.innerHTML = data.map(d => `<article class="card">
                <a class="card-media" href="${d.videoUrl} " target="_blank">
                    <img class="card-thumb" src="${d.videoThumbnail}" loading="lazy">
                </a>
                <div class="card-body">
                    <img class="card-avatar" src="${d.channelLogo}" loading="lazy">
                    <div class="card-meta">
                        <h2 class="card-title">
                            <a href="${d.videoUrl}" target="_blank">${d.videoTitle}</a>
                        </h2>
                        <a class="card-channel" href="${d.channelUrl}" target="_blank">${d.channelTitle}</a>
                    </div>
                </div>
            </article>`).join("");
        })
        .catch(error => console.error('Error:', error));
}

list()
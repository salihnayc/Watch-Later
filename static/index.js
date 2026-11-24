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

function removeVideo(id) {
    const data = new FormData();
    data.append("id", id);
    fetch("/api/remove", {method: "DELETE", body: data})
        .then(() => list());
}

function formatTime(time) {
    time = time.replace("PT", "")
    time = time.replace("H", ":")
    time = time.replace("M", ":")
    time = time.replace("S", "")

    s = time.split(":")

    for (let i = 1; i < s.length; i++) {
        if (s[i].length === 1) s[i] = "0" + s[i]
    }
    return s.join(":")
}

function list() {
    cardHolder.innerHTML = "There are no videos"
    fetch("/api/videos")
        .then(response => response.json())
        .then(data => {
            data.sort((a, b) => a.channelTitle.localeCompare(b.channelTitle, {sensitivity: "base"}) || a.videoTitle.localeCompare(b.videoTitle, {sensitivity: "base"}))
            cardHolder.innerHTML = data.map(d => `<article class="card">
                <a class="card-media" href="${d.videoUrl} " target="_blank">
                    <img class="card-thumb" src="${d.videoThumbnail}" loading="lazy">
                    <span class="card-duration">${formatTime(d.videoDuration)}</span>
                </a>     
                <div class="card-buttons">
                    <button onclick="removeVideo('${d.videoId}')">DELETE</button>
                    <a href="details/${d.videoId}">DETAILS</a>
                </div>
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
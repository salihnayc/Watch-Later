box = document.querySelector("#details-box")

id = document.URL.split("/").slice(-1);

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

function formatDescription(description) {
    return description.replaceAll("\n", "<br />")
}

fetch(`/api/videos/${id}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error.message);
        }
        box.innerHTML = `
            <div class="details-card card">
                <a class="card-media" href="${data.videoUrl} " target="_blank">
                    <img class="card-thumb" src="${data.videoThumbnail}" loading="lazy">
                    <span class="card-duration">${formatTime(data.videoDuration)}</span>
                </a>   
                <div class="card-body">
                    <a class="avatar-link" href="${data.channelUrl}" target="_blank"><img class="card-avatar" src="${data.channelLogo}" loading="lazy"></a>
                    <div class="card-meta">
                        <h2 class="card-title">
                            <a href="${data.videoUrl}" target="_blank">${data.videoTitle}</a>
                        </h2>
                        <a class="card-channel" href="${data.channelUrl}" target="_blank">${data.channelTitle}</a>
                    </div>
                </div> 
            </div>
            <div class="details-side">
                <h3><a href="/"><-- All videos</a></h3>
                <h2>Description</h2>
                <p>${formatDescription(data.videoDescription)}</p>
            </div>
        `
    })
    .catch(error => box.innerHTML = error)
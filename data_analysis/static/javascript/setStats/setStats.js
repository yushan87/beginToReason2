function HTMLStringToElement(text) {
    const parent = document.createElement('div')
    parent.innerHTML = text
    return parent.firstChild
}


//Make cards
const container = document.querySelector("#lessonContainer")
let newCard
for (let lesson of lessonSetData) {
    newCard = HTMLStringToElement(`<div class="col-3" style="margin: 20px 15px; cursor: pointer">
    <div class="card" id="lesson${lesson.lessonID}">
        <div class="card-body">
            <h5 class="card-title">${lesson.title}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${lesson.name}</h6>
            <p class="card-text">
                Average attempts: ${lesson.averageAttempts.toString().substr(0, 4)}<br>
                First try rate: ${(100*lesson.firstTryRate).toString().substr(0, 5)}%<br>
                Completion rate: ${(100 * lesson.completionRate).toString().substr(0, 5)}%<br>
                Users: ${lesson.userCount}
            </p>
        </div>
    </div>
</div>`)
    newCard.onclick = () => {
        window.location.href = `/data_analysis/graph/${lesson.lessonID}`
    }
    container.appendChild(newCard)
}
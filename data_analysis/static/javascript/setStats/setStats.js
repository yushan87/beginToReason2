function HTMLStringToElement(text) {
    const parent = document.createElement('div')
    parent.innerHTML = text
    return parent.firstChild
}


function makeCardText(lesson) {
    cardText = `Average attempts: ${lesson.averageAttempts.toString().substr(0, 4)}`
    cardText += withinBounds(lesson.averageAttempts, "averageAttempts", true)

    cardText += `<br>
    First try rate: ${(100*lesson.firstTryRate).toString().substr(0, 5)}%`
    cardText += withinBounds(lesson.firstTryRate, "firstTryRate", false)

    cardText += `<br>
    Completion rate: ${(100 * lesson.completionRate).toString().substr(0, 5)}%`
    cardText += withinBounds(lesson.completionRate, "completionRate", false)

    cardText += `<br>
    Users: ${lesson.userCount}`

    return cardText
}


/**
 * 
 * @param {float} point 
 * @param {string} type 
 * @param {boolean} highMeansHard 
 * @returns String to be added on
 */
function withinBounds(point, type, highMeansHard) {
    if(point < bounds[type][0]) {
        //Too small!
        if(highMeansHard) {
            return `&nbsp;<img style="position: relative; top: -2px;" src="/static/images/arrow-down-circle-fill-green.svg" data-toggle="tooltip" data-placement="top" title="This was lower than the rest of the set">`
        }
        return `&nbsp;<img style="position: relative; top: -2px;" src="/static/images/arrow-down-circle-fill-red.svg" data-toggle="tooltip" data-placement="top" title="This was lower than the rest of the set">`
    }
    if(point > bounds[type][1]) {
        //Too big!
        if(highMeansHard) {
            return `&nbsp;<img style="position: relative; top: -2px;" src="/static/images/arrow-up-circle-fill-red.svg" data-toggle="tooltip" data-placement="top" title="This was higher than the rest of the set">`
        }
        return `&nbsp;<img style="position: relative; top: -2px;" src="/static/images/arrow-up-circle-fill-green.svg" data-toggle="tooltip" data-placement="top" title="This was higher than the rest of the set">`
    }
    return ""
}


//Make cards
const container = document.querySelector("#lessonContainer")
let newCard
const lessons = lessonSetData["lessons"]
const bounds = lessonSetData["statBounds"]
for (let lesson of lessons) {
    //Throw out lessons that haven't been taken yet
    if (!lesson.userCount) {
        continue
    }
    newCard = HTMLStringToElement(`<div class="col-3" style="margin: 20px 15px; cursor: pointer">
    <div class="card" id="lesson${lesson.lessonID}">
        <div class="card-body">
            <h5 class="card-title">${lesson.title}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${lesson.name}</h6>
            <p class="card-text">
                ${makeCardText(lesson)}
            </p>
        </div>
    </div>
</div>`)
    newCard.onclick = () => {
        window.location.href = `/data_analysis/graph/${lesson.lessonID}`
    }
    container.appendChild(newCard)
}
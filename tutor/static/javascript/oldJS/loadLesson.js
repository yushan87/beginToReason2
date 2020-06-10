/* global ace approved author createEditor resetTime verifying */

var currentLesson;

/**
 * database sends lesson in a json
 * calls parselesson to parse each piece of the lesson
 * */
function loadLessonFromUrl(url) {
    $.getJSON(url, (data) => {
        parseLesson(data);
    });
}

/**
 * separates and sets title, type, and code
 * sets where the information is displayed
 * this is set to work for the old html page
 * this parse will need to be adjusted
 * */
function parseLesson(data) {
    currentLesson = data;

    $("#left .header td").html(data.title);

    $("#left .reference td").html(data.referenceMaterial);
    if (data.type == "tutorial") {
        $("#left .activity td").html(data.activity);
        $("#left .footer").addClass("button");
        $("#left .footer td")
            .html("Tutorial")
            .off("click")
            .click(function () {
                window.open(data.screenCapture, "_blank");
            });
    } else if (data.type == "lesson" || data.type == "challenge") {
        if (typeof data.activity === "undefined") {
            $("#left .activity td").html("Please complete the <b>Confirm</b> assertion(s) and check correctness.");
        } else {
            $("#left .activity td").html(data.activity);
        }
        $("#right .headette").removeClass("button");
        $("#right .headette td").html("").off("click");

    } else if (data.type == "end") {
        $("#left .activity td").html(data.activity);
        $("#endSurvey").click();
    } else {
        $("#left .activity td").html("This should never appear.");
        $("#right .headette").removeClass("button");
        $("#right .headette td").html("").off("click");
    }

    //console.log(data.code)
    createEditor.setValue(data.code);
    createEditor.selection.moveCursorToPosition({
        row: 0,
        column: 0
    });

    createEditor.getSession().setUndoManager(new ace.UndoManager());
    createEditor.getSession().getUndoManager().reset();
}

function endSurvey() {
    $("#dialog-message").html("<b>AuthorID:</b> " + author + "</br></br><b>Instructions:</b></br>Use the number above and complete the survey on Canvas.");
    $("#dialog-box").dialog("open");
}

function reloadLesson() {
    createEditor.setValue(currentLesson.code);
}

function checkLines() {
    var rowNum = createEditor.getCursorPosition().row + 1;

    if (createEditor.selection.isMultiLine()) {
        createEditor.setReadOnly(true);
    } else if ($.inArray(rowNum, currentLesson.lines) != -1) {
        createEditor.setReadOnly(false);
    } else {
        createEditor.setReadOnly(true);
    }
}

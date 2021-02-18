/* global ace */

//////////////////////
// Global Variables //
//////////////////////

let aceEditor; // This is the ACE Editor embedded to the page.
let editorContent = ""; // Content to be displayed in ACE Editor
let Range;
let correctnessChecking = false; // A flag that indicates whether or not the check correctness button has been clicked.
let lineErrorMap; // This contains error information for each line in the current file.
let fontSize; // The current font size
let time = new Date();
let hasFR;
let hasMC;
let darkTheme = true;
let prevAnswers = []; //add to this and check
let name;
let overlayOpen = false;
let allAnswers = "";
let multiAnswer;
let submitAnswers="";
let instructOpen = true;


///////////////////////////////////////
// Main ACE Editor-Related Functions //
///////////////////////////////////////

/*
 * Function for creating and embedding the ACE Editor into our page.
 */
function createEditor(code, explain, lessonName, currIndex, compIndex, review, past) {
    // RESOLVE mode
    let ResolveMode = ace.require("ace/mode/resolve").Mode;
    Range = ace.require("ace/range").Range;

    // Basic editor settings
    aceEditor = ace.edit("editor");
    aceEditor.setTheme("ace/theme/chaos"); //chaos or solarized_light
    fontSize = 20;
    aceEditor.setFontSize(fontSize);
    aceEditor.on("change", checkEdit);

    // Store the content for future use
    editorContent = code;
    name = lessonName;
    aceEditor.session.setValue(editorContent);
    //$("#prev").attr("disabled", "disabled");
    if(review == 'none') {
        document.getElementById("resultCard").style.display = "none";
    }
    else {
        document.getElementById("resultCard").style.display = "block";
        document.getElementById("resultsHeader").innerHTML = "Correct!";
        document.getElementById("resultDetails").innerHTML = review;
        $("#resultCard").attr("class", "card bg-success text-white");

        document.getElementById("answersCard").removeAttribute("hidden")
        document.getElementById("pastAnswers").innerHTML = past;

        $("#resetCode").attr("disabled", "disabled");
        $("#checkCorrectness").attr("disabled", "disabled");
        $("#explainCard").attr("disabled", "disabled");
    }

    //add a check for if need explaination and set hasFR
    //hide or unhide explaination box

    // Set this to RESOLVE mode
    aceEditor.getSession().setMode(new ResolveMode());
    //style = "visibility: hidden"; to hide text area element
    //use if statement to decide if should hide or show and if we need to check if it is full
    if (explain == 'MC') {
        hasFR = false;
        hasMC = true;
    }
    else if (explain == 'Text'){
        hasFR = true;
        hasMC = false;
    }
    else if (explain == 'Both'){
        hasFR = true;
        hasMC = true;
    }
    else {
        hasFR = false;
        hasMC = false;
    }

    if (parseInt(currIndex) < parseInt(compIndex)){
        console.log("HIT")
        console.log("currIndex: " + currIndex + " compIndex: " + compIndex)
        aceEditor.setReadOnly(true)
        $("#resetCode").attr("disabled", "disabled");
        $("#checkCorrectness").attr("disabled", "disabled");
    }
}

/*
* Function for locking all other lines besides confirm
* */
function checkEdit(change) {
    var manager = aceEditor.getSession().getUndoManager();

    // Must wait for the change to filter through the event system. There is
    // probably a way to catch it, but I couldn't find it.
    setTimeout(function () {
        // If it is a multiline change, including removing or adding a line break
        if (change.lines.length > 1) {
            manager.undo(true);
            return;
        }

        // If the line does not have "Confirm" in it somewhere
        // or it's not configured in the "lines". (added by the FAU team)
        if (typeof aceEditor.lines !== "undefined") {
            var rowNum = change.start.row + 1;
            if (!aceEditor.lines.includes(rowNum)) {
                manager.undo(true);
                return;
            }
        } else {
            var line = aceEditor.getSession().getLine(change.start.row);
            if (!line.includes("Confirm") && !line.includes("requires") && !line.includes("ensures")) {
                manager.undo();
                return;
            }
        }
        // Make sure we do not collate undos. Downside: there is no real undo functionality
        manager.reset();
    }, 0);
}


/*
 * Function for creating and embedding the ACE Editor into our page.
 */
function loadLesson(code, explain, lessonName) {
    editorContent = code;
    name = lessonName;
    aceEditor.session.setValue(editorContent);

    if (explain == 'MC') {
        hasFR = false;
        hasMC = true;
    }
    else if (explain == 'Text'){
        hasFR = true;
        hasMC = false;
    }
    else {
        hasFR = true;
        hasMC = true;
    }
}


/*
    Checks for any trivial answers the student may provide, such as "Confirm
    true", "Confirm I = I", or "Confirm I /= I + 1". Returns a list of lines
    and an indicator of trivial or not for each line. Note: may not perfectly
    check for all possible trivials.
*/
function checkForTrivials(content) {
    var lines = content.split("\n");
    var confirms = [];
    var overall = 'success';
    var regex;
    var i;
    var missing = false;

    // Find all the confirm or ensures statements, with their line numbers
    regex = new RegExp("Confirm [^;]*;|ensures [^;]*;", "mg");
    for (i = 0; i < lines.length; i++) {
        var confirm = lines[i].match(regex);
        if (confirm) {
            confirms.push({lineNum: i+1, text: confirm[0], status: 'success'})
        }
    }

    regex = new RegExp("requires [^;]*;" ,"g");
    if (confirms.length == 0 && !regex.test(content)) {
        return {confirms: [], overall: 'failure'}
    }

    for (i = 0; i < confirms.length; i++) {
        // Remove the "Confirm " and "ensures " so that we can find the variable names
        var statement = confirms[i].text;
        statement = statement.substr(8);

        // Search for an illegal "/="
        regex = new RegExp("/=");
        if (statement.search(regex) > -1) {
            overall = 'failure';
            confirms[i].status = "failure";
            continue
        }

        // Split the string at the conditional, first looking for >= and <=
        regex = new RegExp(">=|<=");
        var parts = statement.split(regex);
        if (parts.length > 2) {
            overall = 'failure';
            confirms[i].status = "failure";
            continue
        }

        // If there is no >= or <=
        if (parts.length == 1) {
            regex = new RegExp("=");
            parts = statement.split(regex);
            if (parts.length > 2) {
                overall = 'failure';
                confirms[i].status = "failure";
                continue
            }
        }

        // If there is no >=, <=, or =
        if (parts.length == 1) {
            regex = new RegExp(">|<");
            parts = statement.split(regex);
            if (parts.length != 2) {
                overall = 'failure';
                confirms[i].status = "failure";
                continue
            }
        }

        // Find the variables used on the left side. If there are none, mark it correct.
        var left = parts[0];
        var right = parts[1];
        console.log("left " + left)
        console.log("right " + right)
        regex = new RegExp("[a-np-zA-QS-Z]", "g") // Temporary fix to allow Reverse(#S) o #T on section2, lesson6
        var variables = left.match(regex);
        if (variables === null) {
            overall = 'failure';
            confirms[i].status = "failure";
            continue
        }

        // Search for these variables on the right side
        var j;
        for (j = 0; j < variables.length; j++) {
            var variable = variables[j];
            regex = new RegExp(" " + variable, "g");
            if (right.search(regex) > -1) {
                overall = 'failure';
                confirms[i].status = "failure";
                missing = true;
                continue
            }
        }
    }

    // Get rid of the text field
    for (var confirm of confirms) {
        delete confirm.text
    }
    return {confirms: confirms, overall: overall, missing: missing}
}


////////////////////////////////////
// Editor Alert-Related Functions //
////////////////////////////////////

/*
 * Function for clearing all content in compiler result div.
 */
function clearAlertBox() {
    // Delete compiler result content
    $("#compilerResult").empty();
}

/*
 * Function for creating the proper HTML for rendering an
 * alert box.
 */
function createAlertBox(hasError, message) {
    // New HTML Object #1: Alert Box
    let alertDiv = document.createElement("div");
    alertDiv.setAttribute("id", "resultAlertBox");

    // Change alert box color depending if it has error
    if (hasError) {
        alertDiv.setAttribute("class", "alert alert-danger alert-dismissible mb-0 fade show");
    } else {
        alertDiv.setAttribute("class", "alert alert-secondary alert-dismissible mb-0 fade show");
    }

    // Set other attributes
    alertDiv.setAttribute("role", "alert");
    alertDiv.setAttribute("aria-hidden", "true");

    // New HTML Object #2: Close Button
    let closeButton = document.createElement("button");
    closeButton.setAttribute("type", "button");
    closeButton.setAttribute("class", "close");
    closeButton.setAttribute("data-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");

    // New HTML Object #3: Close Icon
    let closeIconSpan = document.createElement("span");
    closeIconSpan.setAttribute("aria-hidden", "true");
    closeIconSpan.innerHTML = "&times;";

    // Add close icon to close button
    closeButton.appendChild(closeIconSpan);

    // Add message and the close button to the alert box
    alertDiv.appendChild(document.createTextNode(message));
    alertDiv.appendChild(closeButton);

    // Add the alert box to the div
    $("#compilerResult").append(alertDiv);
}


///////////////////////////////
// Toolbar-Related Functions //
///////////////////////////////

/*
 * Function for checking syntax on the current editor contents.
 */
$("#checkCorrectness").click(function () {
    // Lock editor to stop user from making changes
    if (correctnessChecking) {
        return;
    }

    lock();

    /*** Think-aloud: Handle an attempt end ***/



    //is explaination long enough
    if (hasFR) {
        let boxVal = document.forms["usrform"]["comment"].value;
        if (boxVal.length < 10) {
            // Create the appropriate alert box
            let msg = "You must provide a long enough explanation to the right";
            createAlertBox(true, msg);
            $("#explainBox").attr("style", "border: solid red; display: block; width: 100%; resize: none;");
            unlock();
            return;
        }
    }
    let blank = true;
    if (hasMC) {
        let radios = document.getElementsByName('selectExplain');
        for (let i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                blank = false;
                multiAnswer = radios[i].value;
            }
        }
        if (blank){
            let msg = "You must choose an answer to the right";
            createAlertBox(true, msg);
            unlock();
            return;
        }
    }
    document.getElementById("resultCard").style.display = "block";let results = "";
    let code = aceEditor.session.getValue();

    // Check for trivials
    let trivials = checkForTrivials(code);
    if (trivials.overall == "failure") {
        console.log("trivial: " + trivials.trivial )
        if(trivials.missing){
            document.getElementById("resultsHeader").innerHTML = "<h3>Try again</h3>";
            document.getElementById("resultDetails").innerHTML = "Think about the variables in terms of initial values";

        }
        else{
            document.getElementById("resultsHeader").innerHTML = "<h3>Syntax error</h3>";
            document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?";

        }
        $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
        $("#resultCard").attr("class", "card bg-danger text-white");
        //add line errors
        //this will need to be fixed based on verifier return
        //log data

        let currentAttemptAnswers = '';
        for (var i = 0; i < trivials.confirms.length; i++) {
            aceEditor.session.addGutterDecoration(trivials.confirms[i].lineNum-1, "ace_error");
            document.getElementById("answersCard").removeAttribute("hidden")
            allAnswers = allAnswers + aceEditor.session.getLine(trivials.confirms[i].lineNum-1).replace(/\t/g,'') + "<br>";
            currentAttemptAnswers += aceEditor.session.getLine(trivials.confirms[i].lineNum-1).replace(/\t/g,'') + '\n';
            if (i == trivials.confirms.length - 1){
                allAnswers += "<br><br>";
            }
            document.getElementById("pastAnswers").innerHTML = allAnswers;
        }

        closeThinkAloudFunctions(false, 'trivial', currentAttemptAnswers, code); // for the think-aloud recording

        // Unlock editor for further user edits
        unlock();
    }
    else{
        document.getElementById("resultsHeader").innerHTML = "<h3>Checking Correctness...</h3>";
        document.getElementById("resultDetails").innerHTML = '<div class="sk-chase">\n' +
            '  <div class="sk-chase-dot"></div>\n' +
            '  <div class="sk-chase-dot"></div>\n' +
            '  <div class="sk-chase-dot"></div>\n' +
            '  <div class="sk-chase-dot"></div>\n' +
            '  <div class="sk-chase-dot"></div>\n' +
            '  <div class="sk-chase-dot"></div>\n' +
            '</div>';
        $("#resultCard").attr("class", "card text-light");
        $("#resultCard").attr("style", "background: #4C6085");

        verify(code)
    }
});

/*
 * Function for resetting editor's code to the current cached content.
 */
$("#resetCode").click(function () {
    // Lock editor to stop user from making changes
    lock();

    // Put the cached content into the editor
    aceEditor.session.setValue(editorContent);

    // Unlock editor for further user edits
    unlock();

    $('#areYouSure').modal('hide')

    return false;
});

/*
 * Function for retrieving hint
 */
$("#giveHint").click(function () {
    // Lock editor to stop user from making changes
    lock();

    // Create the appropriate alert box
    let hint = "Check the Reference Material to the left of the editor";
    createAlertBox(false, hint);

    // Unlock editor for further user edits
    unlock();
});


$("#changeMode").click(function () {
    // Lock editor to stop user from making changes
    lock();

    if (darkTheme){
        aceEditor.setTheme("ace/theme/solarized_light");
        darkTheme = false;
        $("#changeMode").attr("class", "btn btn-sm btn-dark");
        document.getElementById("changeMode").innerHTML = "<i class=\"fa fa-moon-o\" aria-hidden=\"true\"></i> Dark";
        $("#right-col").attr("style", "background-color: #C8C8C8");
        $("#explainCard").attr("style", "position: absolute;\n" +
            "    bottom: 0;\n" +
            "    width: 98%;\n" +
            "    margin: 5px 5px 5px 5px;\n" +
            "    background-color: #4C6085;\n" +
            "    color: #fff;");
    }
    else {
        aceEditor.setTheme("ace/theme/chaos");
        darkTheme = true;
        $("#changeMode").attr("class", "btn btn-sm btn-light");
        $("#right-col").attr("style", "background-color: #333");
        $("#explainCard").attr("style", "position: absolute;\n" +
            "    bottom: 0;\n" +
            "    width: 98%;\n" +
            "    margin: 5px 5px 5px 5px;\n" +
            "    background-color: #E0E0E0;\n" +
            "    color: #333;");
        document.getElementById("changeMode").innerHTML = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-brightness-high-fill\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
            "  <path d=\"M12 8a4 4 0 1 1-8 0 4 4 0 0 1 8 0z\"/>\n" +
            "  <path fill-rule=\"evenodd\" d=\"M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z\"/>\n" +
            "</svg> Light";
    }

    // Unlock editor for further user edits
    unlock();
});


/*
 * Function for increasing the editor's font size.
 */
$("#fontIncrease").click(function () {
    // Increase font size
    let currentFontSize = $("#editor").css("font-size");
    currentFontSize = parseFloat(currentFontSize) * 1.2;
    $("#editor").css("font-size", currentFontSize);

    return false;
});


/*
 * Function for opening and closing overlay
 */
$("#toggleOverlay").click(function () {
    if(overlayOpen){
        console.log("toggle overlay is true, turning false")
        document.getElementById("myNav").style.width = "0%";
        overlayOpen = false;
        document.getElementById("toggleOverlay").innerHTML = "<i class=\"fa fa-list\" aria-hidden=\"true\"></i> View Lessons";
    }
    else{
        document.getElementById("myNav").style.width = "25%";
        overlayOpen = true;
        document.getElementById("toggleOverlay").innerHTML = "<i class=\"fa fa-times\" aria-hidden=\"true\"></i> Dismiss";
    }
});

$(".toggle-sidebar").click(function () {
    $("#sidebar").toggleClass("collapsed");
    $("#content").toggleClass("col-md-6 col-md-8");
    $("#right-col").toggleClass("col-md-3 col-md-4");
    if(instructOpen){
        document.getElementById("toggleInstruct").innerHTML = "Show Instructions";
        instructOpen = false;
    }
    else{
        document.getElementById("toggleInstruct").innerHTML = "Hide Instructions";
        instructOpen = true;
    }

    return false;
});


/*
 * Function for x of overlay
 */
$("#closeOverlay").click(function () {

        document.getElementById("myNav").style.width = "0%";
        overlayOpen = false;
        document.getElementById("toggleOverlay").innerHTML = "<i class=\"fa fa-list\" aria-hidden=\"true\"></i> View Lessons";

});


/*
 * Function for decreasing the editor's font size.
 */
$("#fontDecrease").click(function () {
    // Decrease font size
    let currentFontSize = $("#editor").css("font-size");
    currentFontSize = parseFloat(currentFontSize) / 1.2;
    $("#editor").css("font-size", currentFontSize);

    return false;
});


$("#lessonList").click(function () {
    console.log( this.innerHTML)

});


/*
 * Function for locking the check syntax and reset buttons.
 */
function lock() {
    clearAlertBox();
    // Lock the editors
    aceEditor.setReadOnly(true);

    // Disable the button and set checkCorrectness to true.
    $("#resetCode").attr("disabled", "disabled");
    correctnessChecking = true;
}

/*
 * Function for unlocking the verify button.
 */
function unlock() {
    // Unlock the editors
    aceEditor.setReadOnly(false);

    // No longer checkCorrectness, so enable the button again.
    correctnessChecking = false;
    $("#resetCode").removeAttr("disabled", "disabled");

    // Focus on the editor.
    aceEditor.focus();
}


///////////////////////////////
// Nav-Related Functions //
///////////////////////////////

/*
 * Function for moving to next lesson.
 */
$("#next").click(function () {
    lock();

    if (activeUploads.count === 0) {
        moveToNextExercise();
    } else {
        activeUploads.registerListener(function (count) {
            if (count === 0) {
                moveToNextExercise();
            }
        });

        setTimeout(function () {
            moveToNextExercise();
        }, 10000);
    }
});

function moveToNextExercise() {
     $.ajax({
        url: 'tutor',
        datatype: 'json',
        type: 'GET',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data) {
            //loadLesson()

        }
    });

     location.reload();
     unlock();
}

/*
 * Function for moving to prev lesson.
 */
$("#prev").click(function () {
    lock();

    $.ajax({
        url: 'completed',
        datatype: 'json',
        type: 'GET',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data) {
            //loadLesson()

        }
    });

    location.reload();
});


/*
$.ajax({
  type: "POST",
  url: "/python/verify.py",
  data: { param: text}
}).done(function( o ) {
   // do something
});
*/

/*
function getTime() {
    var endTime = new Date();
    var result = endTime.getTime() - time.getTime();
    time = endTime;
    return result;
}*/

$.postJSON = (url, data, callback) => {

    return $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response){
            document.getElementById("resultsHeader").innerHTML = response.resultsHeader;
            document.getElementById("resultDetails").innerHTML = response.resultDetails;
            $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");

            if (response.status == "success") {
                $("#resultCard").attr("class", "card bg-success text-white");
                $("#next").removeAttr("disabled", "disabled");
                $("#checkCorrectness").attr("disabled", "disabled");
                closeThinkAloudFunctions(true, 'correct solution', data.answer, data.code); // for the think-aloud recording
                unlock();
                setTimeout(function (){location.reload();}, 3000);
            } else if (response.status == 'failure'){
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-danger text-white");
                closeThinkAloudFunctions(false, 'incorrect solution', data.answer, data.code); // for the think-aloud recording
                unlock();
            } else {
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-danger text-white");
                closeThinkAloudFunctions(false, 'something went wrong',  data.answer, data.code); // for the think-aloud recording
                unlock();
            }
            if (response.reload == "true"){
                setTimeout(function (){location.reload();}, 3000);
            }
            /*
            if(data.sub){
                console.log(data.newLessonIndex)
                console.log(data.newLessonCode)
                loadLesson(data.newLessonCode, 'None',data.newLessonName)
            }

             */
        }

    });
};


function mergeVCsAndLineNums(provedList, lineNums) {
    var overall = 'success';
    var lines = {};

    for (var vc of lineNums) {
        if (provedList[vc.vc] != 'success') {
            overall = 'failure';
        }

        if (lines[vc.lineNum] != 'failure') {
            lines[vc.lineNum] = provedList[vc.vc];
        }
    }

    // Convert from hashtable to array
    var lineArray = [];
    for (var entry of Object.entries(lines)) {
        lineArray.push({'lineNum': entry[0], 'status': entry[1]});
    }

    return {'overall': overall, 'lines': lineArray}
}


/*
    Don't ask, just accept. This is how the Resolve Web API works at the
    moment. If you want to fix this, PLEASE DO.
*/
function encode(data) {
    var regex1 = new RegExp(" ", "g");
    var regex2 = new RegExp("/+", "g");

    var content = encodeURIComponent(data);
    content = content.replace(regex1, "%20");
    content = content.replace(regex2, "%2B");

    var json = {};

    json.name = "BeginToReason";
    json.pkg = "User";
    json.project = "Teaching_Project";
    json.content = content;
    json.parent = "undefined";
    json.type = "f";

    return JSON.stringify(json)
}


function decode(data) {
    var regex1 = new RegExp("%20", "g");
    var regex2 = new RegExp("%2B", "g");
    var regex3 = new RegExp("<vcFile>(.*)</vcFile>", "g");
    var regex4 = new RegExp("\n", "g");

    var content = decodeURIComponent(data)
    content = content.replace(regex1, " ");
    content = content.replace(regex2, "+");
    content = content.replace(regex3, "$1");
    content = decodeURIComponent(content);
    content = decodeURIComponent(content);
    content = content.replace(regex4, "");

    var obj = JSON.parse(content);

    return obj;
}

function verify(code){
    var vcs = {}
    var ws = new WebSocket('wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project');

    // Connection opened
    ws.addEventListener('open', function (event) {
        ws.send(encode(code));
    });

    // Listen for messages
    ws.addEventListener('message', function (event) {
        message = JSON.parse(event.data)
        if (message.status == 'error' || message.status == '') {
            unlock();
            document.getElementById("resultsHeader").innerHTML = "<h3>Syntax error";
            document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?";
            $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
            $("#resultCard").attr("class", "card bg-danger text-white");
            let currentAttemptAnswers = '';
            //add line errors
            //this will need to be fixed based on verifier return
            for (var i = 0; i < message.errors[0].errors.length; i++) {
                aceEditor.session.addGutterDecoration(message.errors[0].errors[i].error.ln - 1, "ace_error")
                document.getElementById("answersCard").removeAttribute("hidden")
                currentAttemptAnswers += aceEditor.session.getLine(message.errors[0].errors[i].error.ln - 1).replace(/\t/g,'')  + "\n";
                var confirmLine = aceEditor.session.getLine(message.errors[0].errors[i].error.ln - 1).replace(/\t/g,'')  + "<br>";
                allAnswers = allAnswers + confirmLine;
                if (i == message.errors[0].errors.length - 1){
                    allAnswers += "<br><br>";
                }
                document.getElementById("pastAnswers").innerHTML = allAnswers;
            }

            closeThinkAloudFunctions(false, 'syntax', currentAttemptAnswers, code); // for the think-aloud recording
        }
        else if (message.status == 'processing') {
            var regex = new RegExp('^Proved')
            if (regex.test(message.result.result)) {
                vcs[message.result.id] = 'success'
            } else {
                vcs[message.result.id] = 'failure'
            }
        }
        else if (message.status == 'complete') {
            ws.close()

            let lineNums = decode(message.result)
            let lines = mergeVCsAndLineNums(vcs, lineNums.vcs)
            var confirmLine
            let vcLine = parseInt(lineNums.vcs[0].lineNum, 10)

            let currentAttemptAnswers = '';
            for (var i = 0; i < lines.lines.length; i++) {
                if (lines.lines[i].status == "success") {
                    aceEditor.session.addGutterDecoration(lines.lines[i].lineNum-1, "ace_correct");
                    confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace(/\s/g,'');
                    confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace("Confirm", "");
                    allAnswers = allAnswers + confirmLine  + "<br>";
                    submitAnswers = submitAnswers + confirmLine;
                    currentAttemptAnswers += confirmLine + '\n'
                }
                else {
                    aceEditor.session.addGutterDecoration(lines.lines[i].lineNum-1, "ace_error");
                    document.getElementById("answersCard").removeAttribute("hidden")
                    confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace(/\s/g,'');
                    confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace("Confirm", "");
                    allAnswers = allAnswers + confirmLine  + "<br>";
                    submitAnswers = submitAnswers + confirmLine;
                    if (i == lines.lines.length - 1){
                    allAnswers += "<br><br>";
                    currentAttemptAnswers += confirmLine + '\n'
                }
                    document.getElementById("pastAnswers").innerHTML = allAnswers;
                }
            }

            /*
            * posting data to back end to log
            * */
            let data = {};
            data.name = name;
            data.answer = submitAnswers;
            data.allAnswers = allAnswers;
            data.code = code;
            if (hasFR){data.explanation = document.forms["usrform"]["comment"].value;}
            else if (hasMC){data.explanation = multiAnswer;}
            else {data.explanation = "No Explaination Requested";}
            data.status = lines.overall;

            const faces = document.querySelectorAll('input[name="smiley"]');
            let selectedValue;
            for (const x of faces) {
                if (x.checked) {
                    selectedValue = x.value;
                    data.face = selectedValue
                }
            }

            $.postJSON("tutor", data, (results) => {});
            submitAnswers = '';

        }
    });
}
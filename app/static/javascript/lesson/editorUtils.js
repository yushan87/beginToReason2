/* global ace */

//////////////////////
// Global Variables //
//////////////////////

var aceEditor; // This is the ACE Editor embedded to the page.
var editorContent = ""; // Content to be displayed in ACE Editor
var correctnessChecking = false; // A flag that indicates whether or not the check correctness button has been clicked.
var fontSize; // The current font size
var time = new Date();

///////////////////////////////////////
// Main ACE Editor-Related Functions //
///////////////////////////////////////

/*
 * Function for creating and embedding the ACE Editor into our page.
 */
function createEditor() {
    // RESOLVE mode
    var ResolveMode = ace.require("ace/mode/resolve").Mode;

    // Basic editor settings
    aceEditor = ace.edit("editor");
    aceEditor.setTheme("ace/theme/tomorrow_night");
    fontSize = 20;
    aceEditor.setFontSize(fontSize);

    // Store the content for future use
    editorContent = "Facility BeginToReason;\n uses Integer_Ext_Theory;\n\n Operation Main();\n Procedure\n Var I, J, K: Integer;\n\n I := 2;\n J := 3;\n\n K := I;\n If (J > I) then\n K := J;\n end;\n\n Confirm K = /*expression*/;\n end Main;\nend BeginToReason;";
    aceEditor.session.setValue(editorContent);

    // Set this to RESOLVE mode
    aceEditor.getSession().setMode(new ResolveMode());
    //style = "visibility: hidden"; to hide text area element
    //use if statement to decide if should hide or show and if we need to check if it is full
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
    var alertDiv = document.createElement("div");
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
    var closeButton = document.createElement("button");
    closeButton.setAttribute("type", "button");
    closeButton.setAttribute("class", "close");
    closeButton.setAttribute("data-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");

    // New HTML Object #3: Close Icon
    var closeIconSpan = document.createElement("span");
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

    //is explaination long enough
    var x = document.forms["usrform"]["comment"].value;
    if (x.length >= 25) {

        /*
        var data = {};

        data.module = currentLesson.module;
        data.name = currentLesson.name;
        data.author = author;
        //data.author = "user.googleId;"   //make userid
        data.milliseconds = getTime();
        data.code = aceEditor.session.getValue();
        //data.explaination = explaination;

        //need to get the answer from the multiple choice
        $.postJSON("/verify", data, (results) => {
            console.log("2");
            if (results.lines !== undefined) {
                addLines(results.lines);
            }

            if (results.status == "trivial") {
                unlock();
                document.getElementById("resultTitle").innerHTML = "Trivial answer";
                document.getElementById("resultDetails").innerHTML = "Try again!";
            } else if (results.status == "unparsable") {
                unlock();
                document.getElementById("resultTitle").innerHTML = "Syntax error";
                document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?";
            } else if (results.status == "failure") {
                if ("problem" in results) {
                    unlock();
                    document.getElementById("resultTitle").innerHTML = "Sorry, not correct";
                    document.getElementById("resultDetails").innerHTML = "Try this other lesson!";
                    //parseLesson(results.problem);
                } else {
                    unlock();
                    document.getElementById("resultTitle").innerHTML = "Wrong answer";
                    document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you read the reference material? <br>2. Do you understand the distinction between #J and J? <br>3. Do you understand the distinction between J and &lt;J&gt;? <br>3. Do you understand the specification parameter modes (e.g. Updates)?";
                }
            } else if (results.status == "success") {
                unlock();
                 document.getElementById("resultTitle").innerHTML = "Correct!";
                 document.getElementById("resultDetails").innerHTML = "On to the next lesson.";
                //console.log(results.problem);
                //parseLesson(results.problem);
            } else {
                unlock();
                document.getElementById("resultTitle").innerHTML = "Something went wrong";
                document.getElementById("resultDetails").innerHTML = "Try again or contact us.";
            }
        });

     */
        $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
        $("#resultCard").attr("class", "card bg-danger text-white");
        document.getElementById("resultTitle").innerHTML = "Syntax error";
        document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?";


    } else {
        // Create the appropriate alert box
        var msg = "You must fill in the explanation box";
        createAlertBox(true, msg);
        $("#explainBox").attr("style", "border: solid red; width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
    }
    // Unlock editor for further user edits
    unlock();
});

/*
 * Function for resetting editor's code to the current cached content.
 */
$("#resetCode").click(function () {
    // Lock editor to stop user from making changes
    lock();
    // Put the cached content into the editor
    aceEditor.session.setValue(editorContent);
    document.forms["usrform"]["comment"].value = "";
    $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
    // Unlock editor for further user edits
    unlock();

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

/*
 * Function for increasing the editor's font size.
 */
$("#fontIncrease").click(function () {
    // Increase font size
    var currentFontSize = $("#editor").css("font-size");
    currentFontSize = parseFloat(currentFontSize) * 1.2;
    $("#editor").css("font-size", currentFontSize);

    return false;
});

/*
 * Function for decreasing the editor's font size.
 */
$("#fontDecrease").click(function () {
    // Decrease font size
    var currentFontSize = $("#editor").css("font-size");
    currentFontSize = parseFloat(currentFontSize) / 1.2;
    $("#editor").css("font-size", currentFontSize);

    return false;
});

/*
 * Function for reset the editor's font size.
 */
$("#resetFontSize").click(function () {
    // Reset font size
    $("#editor").css("font-size", fontSize);

    return false;
});

/*
 * Function for locking the check syntax and reset buttons.
 */
function lock() {
    clearAlertBox();
    // Lock the editors
    aceEditor.setReadOnly(true);

    // Disable the button and set checkCorrectness to true.
    $("#checkCorrectness").attr("disabled", "disabled");
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
    $("#checkCorrectness").removeAttr("disabled", "disabled");
    $("#resetCode").removeAttr("disabled", "disabled");

    // Focus on the editor.
    aceEditor.focus();
}

/*
function getTime() {
    var endTime = new Date();
    var result = endTime.getTime() - time.getTime();
    time = endTime;
    return result;
}

$.postJSON = (url, data, callback) => {
    return $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: callback
    });
};*/

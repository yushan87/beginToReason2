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
let progressCounter = 0;
let darkTheme = true;
let prevAnswers = []; //add to this and check
let name


///////////////////////////
// Arrays in Place of DB //
///////////////////////////
let codeArray = ["Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n    Var I, J, K: Integer;\n\n    I := 2;\n    J := 3;\n\n    K := I;\n    If (J > I) then\n    K := J;\n    end;\n\n    Confirm K = /*expression*/;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I /*conditional*/ #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = /*expression*/;\n    end Main;\nend BeginToReason;"];
let sucArray = ["Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n    Var I, J, K: Integer;\n\n    I := 2;\n    J := 3;\n\n    K := I;\n    If (J > I) then\n    K := J;\n    end;\n\n    Confirm K = 3;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I > #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = #I + 1;\n    end Main;\nend BeginToReason;"];
let failArray = ["Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n    Var I, J, K: Integer;\n\n    I := 2;\n    J := 3;\n\n    K := I;\n    If (J > I) then\n    K := J;\n    end;\n\n    Confirm K = 2;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I < #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = #I;\n    end Main;\nend BeginToReason;"];
let trivialArray = ["Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n    Var I, J, K: Integer;\n\n    I := 2;\n    J := 3;\n\n    K := I;\n    If (J > I) then\n    K := J;\n    end;\n\n    Confirm K = /*expression*/;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I /*conditional*/ #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = /*expression*/;\n    end Main;\nend BeginToReason;"];

let codeCounter = 0;
let sucCounter = 0;
let failCounter = 0;
let trivialCounter = 0;


///////////////////////////////////////
// Main ACE Editor-Related Functions //
///////////////////////////////////////

/*
 * Function for creating and embedding the ACE Editor into our page.
 */
function createEditor(code, explain, lessonName) {
    // RESOLVE mode
    let ResolveMode = ace.require("ace/mode/resolve").Mode;
    Range = ace.require("ace/range").Range;

    // Basic editor settings
    aceEditor = ace.edit("editor");
    aceEditor.setTheme("ace/theme/chaos"); //chaos or solarized_light
    fontSize = 20;
    aceEditor.setFontSize(fontSize);

    // Store the content for future use
    editorContent = code;
    name = lessonName;
    aceEditor.session.setValue(editorContent);
    $("#prev").attr("disabled", "disabled");
    document.getElementById("resultCard").style.display = "none";

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
    else {
        hasFR = true;
        hasMC = true;
    }
}

function encode(data) {
    var regex1 = new RegExp(" ", "g")
    var regex2 = new RegExp("/+", "g")

    var content = encodeURIComponent(data)
    content = content.replace(regex1, "%20")
    content = content.replace(regex2, "%2B")

    var json = {}

    json.name = "BeginToReason"
    json.pkg = "User"
    json.project = "Teaching_Project"
    json.content = content
    json.parent = "undefined"
    json.type = "f"

    console.log( JSON.stringify(json))
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

    //is explaination long enough
    let boxVal = document.forms["usrform"]["comment"].value;
    if (hasFR && boxVal.length < 0) {
        // Create the appropriate alert box
        let msg = "You must fill in the your explanation to the right";
        createAlertBox(true, msg);
        $("#explainBox").attr("style", "border: solid red; display: block; width: 100%; resize: none;");

    } else {
        document.getElementById("resultCard").style.display = "block";



        //need some kind of post to send code to views

        //add check for trivials
        //use code from verify.js



        let results = "";
        let code = aceEditor.session.getValue();
        let data = {};
        //data.module = currentLesson.module;
        data.name = name;
        //data.author = author;
        //data.author = "user.googleId;"   //make userid
        //data.milliseconds = getTime();
        data.code = code;
        data.explanation = document.forms["usrform"]["comment"].value;

        encode(code);

        $.postJSON("tutor", data, (results) => {
            /*if (results.lines !== undefined) {
                addLines(results.lines);
            }*/

            if (results.status == "trivial") {
                document.getElementById("resultsHeader").innerHTML = "Trivial answer";
                document.getElementById("resultDetails").innerHTML = "Try again!";
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-danger text-white");
                //add line errors
                //this will need to be fixed based on verifier return
            } else if (results.status == "unparsable") {
                document.getElementById("resultsHeader").innerHTML = "Syntax error";
                document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?";
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-danger text-white");
                //add line errors
                //this will need to be fixed based on verifier return
            } else if (results.status == "failure") {
                document.getElementById("resultsHeader").innerHTML = "Wrong answer";
                document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you read the reference material? <br>2. Do you understand the distinction between #J and J? <br>3. Do you understand the distinction between J and &lt;J&gt;? <br>3. Do you understand the specification parameter modes (e.g. Updates)?";
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-danger text-white");
                //add line errors
                //this will need to be fixed based on verifier return
            } else if (results.status == "success") {
                document.getElementById("resultsHeader").innerHTML = "Correct!";
                document.getElementById("resultDetails").innerHTML = "On to the next lesson.";
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-success text-white");
                $("#next").removeAttr("disabled", "disabled");
                $("#checkCorrectness").attr("disabled", "disabled");
                // aceEditor.session.addGutterDecoration(need this from views/verifier, "ace_correct");
            } else {
                document.getElementById("resultsHeader").innerHTML = "Something went wrong";
                document.getElementById("resultDetails").innerHTML = "Try again or contact us.";
                $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
                $("#resultCard").attr("class", "card bg-danger text-white");
            }
        });
    };
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
    if (hasFR) {
        document.forms["usrform"]["comment"].value = "";
        $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
    }

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
        $("#right-col").attr("style", "background-color: #E0E0E0");
        $("#explainCard").attr("style", "position: absolute;\n" +
            "    bottom: 0;\n" +
            "    width: 98%;\n" +
            "    margin: 5px 5px 5px 5px;\n" +
            "    background-color: #333;\n" +
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
 * Function for decreasing the editor's font size.
 */
$("#fontDecrease").click(function () {
    // Decrease font size
    let currentFontSize = $("#editor").css("font-size");
    currentFontSize = parseFloat(currentFontSize) / 1.2;
    $("#editor").css("font-size", currentFontSize);

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

    //loadLesson()
    unlock();

return;

console.log("after return")

    //take away line errors
    if (codeCounter == 0) {
        aceEditor.session.removeGutterDecoration(15, "ace_correct");
    } else if (codeCounter == 1) {
        aceEditor.session.removeGutterDecoration(11, "ace_correct");
    } else if (codeCounter == 2) {
        aceEditor.session.removeGutterDecoration(11, "ace_correct");
    }

    codeCounter++;
    sucCounter++;
    failCounter++;
    trivialCounter++;
    progressCounter++;

    if (codeCounter < codeArray.length) {

        if (codeCounter != 0) {
            $("#prev").removeAttr("disabled", "disabled");
        }

        document.getElementById("resultCard").style.display = "none";
        editorContent = codeArray[codeCounter];
        aceEditor.session.setValue(editorContent);
        if (hasFR){
            document.forms["usrform"]["comment"].value = "";
            $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
        }
        document.getElementById("resultsHeader").innerHTML = "";
        document.getElementById("resultDetails").innerHTML = "";
        $("#resultCard").attr("class", "card bg-light");
        $("#next").attr("disabled", "disabled");
        $("#checkCorrectness").removeAttr("disabled", "disabled");

        //progress increaser
        if (progressCounter == 1) {
            $("#lesson1").attr("class", "active");
        } else if (progressCounter == 2) {
            $("#lesson2").attr("class", "active");
        }
    } else {
        //add something in db for what was completed then you can go through them
        document.getElementById("resultsHeader").innerHTML = "Congratulations";
        document.getElementById("resultDetails").innerHTML = "You've completed all the activities";
        $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
        $("#resultCard").attr("class", "card bg-dark text-white");
        $("#next").attr("disabled", "disabled");
        $("#checkCorrectness").removeAttr("disabled", "disabled");
        editorContent = "No more activities";
        aceEditor.session.setValue(editorContent);


        if (progressCounter == 3) {
            $("#lesson3").attr("class", "active");
        }
    }

    unlock();
    return false;
});

/*
 * Function for moving to prev lesson.
 */
$("#prev").click(function () {
    lock();

    //take away line errors
    if (codeCounter == 0) {
        aceEditor.session.removeGutterDecoration(15, "ace_correct");
    } else if (codeCounter == 1) {
        aceEditor.session.removeGutterDecoration(11, "ace_correct");
    } else if (codeCounter == 2) {
        aceEditor.session.removeGutterDecoration(11, "ace_correct");
    }

    codeCounter--;
    sucCounter--;
    failCounter--;
    trivialCounter--;
    progressCounter--;

    if (codeCounter < codeArray.length) {

        if (codeCounter == 0) {
            $("#prev").attr("disabled", "disabled");
        }
        document.getElementById("resultCard").style.display = "none";
        editorContent = codeArray[codeCounter];
        aceEditor.session.setValue(editorContent);
        if (hasFR) {
            document.forms["usrform"]["comment"].value = "";
            $("#explainBox").attr("style", "display: block; width: 100%; resize: none;");
        }
        document.getElementById("resultsHeader").innerHTML = "";
        document.getElementById("resultDetails").innerHTML = "";
        $("#resultCard").attr("class", "card bg-light");
        $("#next").removeAttr("disabled", "disabled");

    }

    unlock();
    return false;
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
        success: callback
    });
};

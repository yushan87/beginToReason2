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
let hasExplanation = false;
let progressCounter = 0;
let darkTheme = true;
let prevAnswers = []; //add to this and check


///////////////////////////
// Arrays in Place of DB //
///////////////////////////
let codeArray = ["Facility BeginToReason;\n uses Integer_Ext_Theory;\n\n Operation Main();\n Procedure\n Var I, J, K: Integer;\n\n I := 2;\n J := 3;\n\n K := I;\n If (J > I) then\n K := J;\n end;\n\n Confirm K = /*expression*/;\n end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I /*conditional*/ #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = /*expression*/;\n    end Main;\nend BeginToReason;"];
let activityArray = ["<p>Please complete the <b>Confirm</b> assertion(s) by entering an expression for /* expression */, then check correctness. <br><br> Answer in terms of variables.</p>", "<p>Please complete the <b>Confirm</b> assertion(s) by choosing a conditional operator to replace the /* conditional */, then check correctness.</p>", "<p>Please complete the <b>Confirm</b> assertion(s) by entering an expression for /* expression */, then check correctness.</p>"];
let refArray = ["<p><code>:= </code> is the <em>assignment operator</em></p>", "<p>At the place marked by <b>Remember</b>, values of variables such as I and J are assumed to be #I and #J.</p><p>Conditional operators are:<br />=, &lt;, &lt;=, &gt;, &gt;=</p>", "<p>At the place marked by <b>Remember</b>, values of variables such as I and J are assumed to be #I and #J.</p>"];
let sucArray = ["Facility BeginToReason;\n uses Integer_Ext_Theory;\n\n Operation Main();\n Procedure\n Var I, J, K: Integer;\n\n I := 2;\n J := 3;\n\n K := I;\n If (J > I) then\n K := J;\n end;\n\n Confirm K = 3;\n end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I > #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = #I + 1;\n    end Main;\nend BeginToReason;"];
let failArray = ["Facility BeginToReason;\n uses Integer_Ext_Theory;\n\n Operation Main();\n Procedure\n Var I, J, K: Integer;\n\n I := 2;\n J := 3;\n\n K := I;\n If (J > I) then\n K := J;\n end;\n\n Confirm K = 2;\n end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I < #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = #I;\n    end Main;\nend BeginToReason;"];
let trivialArray = ["Facility BeginToReason;\n uses Integer_Ext_Theory;\n\n Operation Main();\n Procedure\n Var I, J, K: Integer;\n\n I := 2;\n J := 3;\n\n K := I;\n If (J > I) then\n K := J;\n end;\n\n Confirm K = /*expression*/;\n end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1; -- Assignment\n\n        Confirm I /*conditional*/ #I;\n    end Main;\nend BeginToReason;", "Facility BeginToReason;\n    uses Integer_Ext_Theory;\n\n    Operation Main();\n    Procedure\n        Var I: Integer;\n        Read(I);\n        Remember;\n\n        I := I + 1;\n\n        Confirm I = /*expression*/;\n    end Main;\nend BeginToReason;"];

let codeCounter = 0;
let activityCounter = 0;
let refCounter = 0;
let sucCounter = 0;
let failCounter = 0;
let trivialCounter = 0;


///////////////////////////////////////
// Main ACE Editor-Related Functions //
///////////////////////////////////////

/*
 * Function for creating and embedding the ACE Editor into our page.
 */
function createEditor() {
    // RESOLVE mode
    let ResolveMode = ace.require("ace/mode/resolve").Mode;
    Range = ace.require("ace/range").Range;

    // Basic editor settings
    aceEditor = ace.edit("editor");
    aceEditor.setTheme("ace/theme/chaos"); //chaos or solarized_light
    fontSize = 20;
    aceEditor.setFontSize(fontSize);

    // Store the content for future use
    editorContent = codeArray[codeCounter];
    aceEditor.session.setValue(editorContent);
    document.getElementById("activity").innerHTML = activityArray[activityCounter];
    document.getElementById("referenceMaterial").innerHTML = refArray[refCounter];
    document.getElementById("about").innerHTML = "This system uses simple activities to understand the difficulties students face in reasoning logically about code, so that instruction can be improved.";
    $("#prev").attr("disabled", "disabled");
    document.getElementById("resultCard").style.display = "none";

    //add a check for if need explaination and set hasExplanation
    //hide or unhide explaination box

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
    if (hasExplanation && boxVal.length < 25) {
        // Create the appropriate alert box
        let msg = "You must fill in the explanation box";
        createAlertBox(true, msg);
        $("#explainBox").attr("style", "border: solid red; width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");

    } else {
        document.getElementById("resultCard").style.display = "block";

        let results = "";
        let code = aceEditor.session.getValue();

        if (code == trivialArray[trivialCounter]) {
            results = "trivial";
        } else if (code == failArray[failCounter]) {
            results = "failure";
        } else if (code == sucArray[sucCounter]) {
            results = "success";
        }

        if (results == "trivial") {
            unlock();
            document.getElementById("resultTitle").innerHTML = "Trivial answer";
            document.getElementById("resultDetails").innerHTML = "Try again!";
            $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
            $("#resultCard").attr("class", "card bg-danger text-white");
            //add line errors
            //this will need to be fixed based on verifier return
            if (codeCounter == 0) {
                aceEditor.session.addGutterDecoration(15, "ace_error");
            } else if (codeCounter == 1) {
                aceEditor.session.addGutterDecoration(11, "ace_error");
            } else if (codeCounter == 2) {
                aceEditor.session.addGutterDecoration(11, "ace_error");
            }

        } else if (results == "unparsable") {
            unlock();
            document.getElementById("resultTitle").innerHTML = "Syntax error";
            document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?";
            $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
            $("#resultCard").attr("class", "card bg-danger text-white");
            //add line errors
            //this will need to be fixed based on verifier return
            if (codeCounter == 0) {
                aceEditor.session.addGutterDecoration(15, "ace_error");
            } else if (codeCounter == 1) {
                aceEditor.session.addGutterDecoration(11, "ace_error");
            } else if (codeCounter == 2) {
                aceEditor.session.addGutterDecoration(11, "ace_error");
            }

        } else if (results == "failure") {
            unlock();
            document.getElementById("resultTitle").innerHTML = "Wrong answer";
            document.getElementById("resultDetails").innerHTML = "Check each of the following: <br>1. Did you read the reference material? <br>2. Do you understand the distinction between #J and J? <br>3. Do you understand the distinction between J and &lt;J&gt;? <br>3. Do you understand the specification parameter modes (e.g. Updates)?";
            $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
            $("#resultCard").attr("class", "card bg-danger text-white");
            //add line errors
            //this will need to be fixed based on verifier return
            if (codeCounter == 0) {
                aceEditor.session.addGutterDecoration(15, "ace_error");
            } else if (codeCounter == 1) {
                aceEditor.session.addGutterDecoration(11, "ace_error");
            } else if (codeCounter == 2) {
                aceEditor.session.addGutterDecoration(11, "ace_error");
            }

        } else if (results == "success") {
            unlock();
            document.getElementById("resultTitle").innerHTML = "Correct!";
            document.getElementById("resultDetails").innerHTML = "On to the next lesson.";
            $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
            $("#resultCard").attr("class", "card bg-success text-white");
            $("#next").removeAttr("disabled", "disabled");
            //take away line errors
            if (codeCounter == 0) {
                aceEditor.session.removeGutterDecoration(15, "ace_error");
                aceEditor.session.addGutterDecoration(15, "ace_correct");
            } else if (codeCounter == 1) {
                aceEditor.session.removeGutterDecoration(11, "ace_error");
                aceEditor.session.addGutterDecoration(11, "ace_correct");
            } else if (codeCounter == 2) {
                aceEditor.session.removeGutterDecoration(11, "ace_error");
                aceEditor.session.addGutterDecoration(11, "ace_correct");
            }
        } else {
            unlock();
            document.getElementById("resultTitle").innerHTML = "Something went wrong";
            document.getElementById("resultDetails").innerHTML = "Try again or contact us.";
            $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
            $("#resultCard").attr("class", "card bg-danger text-white");
        }
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
    //take away line errors
    if (codeCounter == 0) {
        aceEditor.session.removeGutterDecoration(15, "ace_error");
    } else if (codeCounter == 1) {
        aceEditor.session.removeGutterDecoration(11, "ace_error");
    } else if (codeCounter == 2) {
        aceEditor.session.removeGutterDecoration(11, "ace_error");
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
        document.getElementById("changeMode").innerHTML = "<i class=\"fa fa-moon-o\" aria-hidden=\"true\"></i>";
    }
    else {
        aceEditor.setTheme("ace/theme/chaos");
        darkTheme = true;
        $("#changeMode").attr("class", "btn btn-sm btn-light");
        document.getElementById("changeMode").innerHTML = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-brightness-high-fill\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
            "  <path d=\"M12 8a4 4 0 1 1-8 0 4 4 0 0 1 8 0z\"/>\n" +
            "  <path fill-rule=\"evenodd\" d=\"M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z\"/>\n" +
            "</svg>";
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


///////////////////////////////
// Nav-Related Functions //
///////////////////////////////

/*
 * Function for moving to next lesson.
 */
$("#next").click(function () {
    lock();

    //take away line errors
    if (codeCounter == 0) {
        aceEditor.session.removeGutterDecoration(15, "ace_correct");
    } else if (codeCounter == 1) {
        aceEditor.session.removeGutterDecoration(11, "ace_correct");
    } else if (codeCounter == 2) {
        aceEditor.session.removeGutterDecoration(11, "ace_correct");
    }

    codeCounter++;
    activityCounter++;
    refCounter++;
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
        document.getElementById("activity").innerHTML = activityArray[activityCounter];
        document.getElementById("referenceMaterial").innerHTML = refArray[refCounter];
        document.forms["usrform"]["comment"].value = "";
        $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
        document.getElementById("resultTitle").innerHTML = "";
        document.getElementById("resultDetails").innerHTML = "";
        $("#resultCard").attr("class", "card bg-light");
        $("#next").attr("disabled", "disabled");

        //progress increaser
        if (progressCounter == 1) {
            $("#lesson1").attr("class", "active");
        } else if (progressCounter == 2) {
            $("#lesson2").attr("class", "active");
        }
    } else {
        //add something in db for what was completed then you can go through them
        document.getElementById("resultTitle").innerHTML = "Congratulations";
        document.getElementById("resultDetails").innerHTML = "You've completed all the activities";
        $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
        $("#resultCard").attr("class", "card bg-dark text-white");
        $("#next").attr("disabled", "disabled");
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
    activityCounter--;
    refCounter--;
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
        document.getElementById("activity").innerHTML = activityArray[activityCounter];
        document.getElementById("referenceMaterial").innerHTML = refArray[refCounter];
        document.forms["usrform"]["comment"].value = "";
        $("#explainBox").attr("style", "width: 90%; resize: none; display: block; margin-left: auto; margin-right: auto;");
        document.getElementById("resultTitle").innerHTML = "";
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

/* global ace */

//////////////////////
// Global Variables //
//////////////////////

var aceEditor; // This is the ACE Editor embedded to the page.
var editorContent = ""; // Content to be displayed in ACE Editor
var correctnessChecking = false; // A flag that indicates whether or not the check correctness button has been clicked.
var fontSize; // The current font size

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
    fontSize = 16;
    aceEditor.setFontSize(fontSize);

    // Store the content for future use
    editorContent = "-- Try adding some RESOLVE code here!";
    aceEditor.session.setValue(editorContent);

    // Set this to RESOLVE mode
    aceEditor.getSession().setMode(new ResolveMode());
}


///////////////////////////////
// Toolbar-Related Functions //
///////////////////////////////

/*
 * Function for checking syntax on the current editor contents.
 */
$("#checkCorrectness").click(function () {
    // Lock editor to stop user from making changes
    lock();

    // Code for checking correctness goes here

    // Unlock editor for further user edits
    unlock();

    return false;
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

    return false;
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

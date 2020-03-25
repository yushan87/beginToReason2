/* global addLines author createEditor currentLesson parseLesson */

var verifying = false;
var time = new Date();

/**
* To be called when "check correctness" is pressed
* locks the page, retrieves the code from the editor,
* calls verify to see if code is correct
* result of verify is stored in "results.status"
* error messages or success message is then sent to page
*
*
* */
function submit() {

//this is a popup prompt to get explaination from use
/**  var bool = 0;
  var explaination = prompt("Please explain your reasoning for your answer: ", "");
  while(bool == 0){
    if (explaination == null || explaination == "") {
      bool = 0;
      explaination = prompt("Please explain your reasoning before pressing ok: ", "");
    }
    else {
      bool = 1;
    }
  }*/

    /* Protect against multiple requests */
    if (verifying) {
        return;
    }
    lock();

    var data = {};
    data.module = currentLesson.module;
    data.name = currentLesson.name;
    data.author = author;
    //data.author = "user.googleId;"   //make userid
    data.milliseconds = getTime();
    data.code = createEditor.getValue();
    data.explaination = explaination;
    //need to get the answer from the multiple choice
    $.postJSON("/verify", data, (results) => {
        if (results.lines !== undefined) {
            addLines(results.lines);
        }

        if (results.status == "trivial") {
            unlock("Trivial answer. Try again!");
        } else if (results.status == "unparsable") {
            unlock("<b>Syntax error.</b> <br>Check each of the following: <br>1. Did you fill out all confirm assertions? <br>2. Is there a semicolon at the end of each assertion? <br>3. Did you use the correct variable names?");
        } else if (results.status == "failure") {
            if ("problem" in results) {
                unlock("Sorry, not correct. Try this other lesson!");
                parseLesson(results.problem);
            } else {
                unlock("<b>Wrong answer.</b> <br>Check each of the following: <br>1. Did you read the reference material? <br>2. Do you understand the distinction between #J and J? <br>3. Do you understand the distinction between J and &lt;J&gt;? <br>3. Do you understand the specification parameter modes (e.g. Updates)?");
            }
        } else if (results.status == "success") {
            unlock("Correct! On to the next lesson.");
            //console.log(results.problem);
            parseLesson(results.problem);
        } else {
            unlock("Something went wrong.");
        }
    });
}

/**
* lock ensures nothing can be done on the page while verifying
* */
function lock() {
    verifying = true;
    $("#right .footette").attr("class", "footetteDisabled");
}

/**
* unlock reopens the page to be typed on
* */
function unlock(message) {
    $("#dialog-message").html(message);
    $("#dialog-box").dialog("open");
    verifying = false;
    $("#right .footetteDisabled").attr("class", "footette");
    createEditor.focus();
}

/**
    Gets the number of milliseconds since the last time this function was
    called, or since the page loaded if it is the first call.
*/
function getTime() {
    var endTime = new Date();
    var result = endTime.getTime() - time.getTime();
    time = endTime;
    return result;
}

/**
    Really, why does this not exist?
*/
$.postJSON = (url, data, callback) => {
    return $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: callback
    });
};

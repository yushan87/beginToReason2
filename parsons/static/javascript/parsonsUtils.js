let isDarkTheme = true;
let width;
let height;
let font = 19;
let previousAnswers = "";
let answerInd = 1;
let placeholderInd;
let lineNumber = 1;
let parsonsSpaces = "";

let keywords = ["Facility", "uses", "Operation", "Var", "Remember", "Confirm", "end", "If", "then", "else", "do", "changing", "decreasing", "increasing", "While", "For", "ProcedureVar"];
let operations = ["<", "&gt;", ">", "&lt;" , "<=",">=", "&gt;=", "&lt;=", "/=", "=", "+", "-", "*", "/", ":=", ":", "="];

function getParsonsFeedback (event, beginSet, endSet, parson, comments) {
    let answeredQuestion = true;

    if (hasFR) {
        let boxVal = document.forms["usrform"]["comment"].value;
        if (boxVal.length < 10) {
            // Create the appropriate alert box
            let msg = "You must provide a long enough explanation to the right";
            createAlertBox(true, msg);
            $("#explainBox").attr("style", "border: solid red; display: block; width: 100%; resize: none;");

            answeredQuestion = false;
        }
    }
    let blank = true;
    if (hasMC) {
        let radios = document.getElementsByName('selectExplain');
        for (let i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                blank = false;
                multiAnswer = radios[i].value;
                
                answeredQuestion = true
            }
        }
        if (blank){
            let msg = "You must choose an answer to the right";
            createAlertBox(true, msg);
            answeredQuestion = false;
        }
    }

    if (answeredQuestion) {
        event.preventDefault();

        let organizedCode = document.getElementById("ul-sortable").querySelectorAll('li');
        
        let answers = [];
        previousAnswers += answerInd + ". ";
        answerInd++;
        organizedCode.forEach((item, index) => {
            let nextAnswer = "";
            nextAnswer = nextAnswer + $('span', item).text();
            nextAnswer = nextAnswer + '\n';
            answers.push(nextAnswer);
            if (index != 0) {
                previousAnswers += "&nbsp&nbsp&nbsp" + nextAnswer + "<br/>";
            }
            else {
                previousAnswers += nextAnswer + "<br/>";
            }
        })

        
        console.log(comments);
        comments = comments.replaceAll("&#x27;", "");
        comments = comments.replace("[", "");
        comments = comments.replace("]", "");
        let commentArr = comments.split(',');
        let commentInd = 0;

        answers.forEach((element, index) => {
            console.log(index);
            if (answers[index].includes("While") || answers[index].includes("For")) {
                doInd = answers[index].indexOf(" do");
                answers[index] = answers[index].substring(0, doInd) + commentArr[commentInd] + answers[index].substring(doInd, answers[index].len);
                commentInd++;
            }
        })

        let totalAnswerLen = 0;
        for (var i = 0; i < answers.length; ++i) {
            totalAnswerLen = totalAnswerLen + answers[i].length;
        }

        studentCode = beginSet;
        for (var i = 0; i < answers.length; ++i) {
            studentCode += answers[i];
        }
        studentCode += endSet;

        studentCode = studentCode.split("&gt;").join(">");
        studentCode = studentCode.split("&lt;").join("<");

        console.log(studentCode);

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

        feedback = parson.getFeedback();

        if (feedback[0] == "Remember to use proper code style and indentation.") {
            document.getElementById("resultCard").style.display = "block";
            document.getElementById("resultsHeader").innerHTML = "Try Again!";
            document.getElementById("resultDetails").innerHTML = feedback[0];
            $("#resultCard").attr("class", "card bg-danger text-white");
        }

        else {
            verify(studentCode);
        }
    }
}


function getMulitConfirmFeedback (event, beginSet, endSet, confirms, comments) {
    let answeredQuestion = true;

    if (hasFR) {
        let boxVal = document.forms["usrform"]["comment"].value;
        if (boxVal.length < 10) {
            // Create the appropriate alert box
            let msg = "You must provide a long enough explanation to the right";
            createAlertBox(true, msg);
            $("#explainBox").attr("style", "border: solid red; display: block; width: 100%; resize: none;");

            answeredQuestion = false;
        }
    }
    let blank = true;
    if (hasMC) {
        let radios = document.getElementsByName('selectExplain');
        for (let i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                blank = false;
                multiAnswer = radios[i].value;
                
                answeredQuestion = true
            }
        }
        if (blank){
            let msg = "You must choose an answer to the right";
            createAlertBox(true, msg);
            answeredQuestion = false;
        }
    }

    if (answeredQuestion) {
        event.preventDefault();

        let lists = document.getElementsByTagName("ul");
        let sortables = [];
        for (var i = 0; i < lists.length; ++i) {
            if (lists[i].id.includes("ul-sortable") && lists[i].id != "ul-sortableTrash") {
                sortables.push(document.getElementById(lists[i].id));
            }
        }

        comments = comments.replaceAll("&#x27;", "");
        comments = comments.replace("[", "");
        comments = comments.replace("]", "");
        let commentArr = comments.split(',');
        let commentInd = 0;

        previousAnswers += answerInd + ". ";
        answerInd++;

        answers = [];
        for (var i = 0; i < sortables.length; ++i) {
            answers.push("");
            for (var j = 0; j < sortables[i].childElementCount; ++j) {
                if (sortables[i].childNodes[j].innerText != undefined) {
                    if (sortables[i].childNodes[j].innerText.includes("While") || sortables[i].childNodes[j].innerText.includes("For")) {
                        doInd = sortables[i].childNodes[j].innerText.indexOf(" do");
                        answer = sortables[i].childNodes[j].innerText.substring(0, doInd) + commentArr[commentInd] + sortables[i].childNodes[j].innerText.substring(doInd, sortables[i].childNodes[j].innerText.len);
                        commentInd++;
                    }
                    else {
                        answer = sortables[i].childNodes[j].innerText;
                    }
                    answers[i] += answer + "\n";

                    if (i != 0 || j != 0) {
                        previousAnswers += "&nbsp&nbsp&nbsp" + sortables[i].childNodes[j].innerText + "<br/>";
                    }
                    else {
                        previousAnswers += sortables[i].childNodes[j].innerText + "<br/>";
                    }
                }
            }
        }

        confirms = confirms.replaceAll("&#x27;", "");
        confirms = confirms.replaceAll(/\\t/g, "");
        confirms = confirms.replaceAll(/\\n/g, '\n');
        confirms = confirms.replace("[", "");
        confirms = confirms.replace("]", "");
        let confirmArr = confirms.split(',');

        studentCode = beginSet;
        for (var i = 0; i < confirmArr.length; ++i) {
            studentCode += answers[i];
            studentCode += confirmArr[i];
        }
        studentCode += endSet;

        studentCode = studentCode.split("&gt;").join(">");
        studentCode = studentCode.split("&lt;").join("<");
        studentCode = studentCode.replaceAll(/\\n/g, "");

        console.log(studentCode);

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

        verify(studentCode);
    }
}

function changeTheme() {
    if (isDarkTheme) {
        isDarkTheme = false;

        $(".codeContainer").attr("style", "background-color: #f0f0f0;\n" + 
                                            "width: " + width + "px;\n" +
                                            "height: " + height + "px;");

        $(".keyword").attr("style", "color: #000bff;");
        $(".operation").attr("style", "color: #000bff;");
        $(".number").attr("style", "color: #b33600;");
        $(".text").attr("style", "color: #3a4958;");

        $(".sortable-code").attr("style", "color: #3a4958;");

        $("ul.output").attr("style", "background-color: rgb(196, 195, 119);");
        $(".sortable-code li").attr("style", "background-color: rgb(196, 195, 119);");
    }

    else {
        isDarkTheme = true;

        $(".codeContainer").attr("style", "background-color: #161616;\n" + 
                                            "width: " + width + "px;\n" +
                                            "height: " + height + "px;");

        $(".keyword").attr("style", "color: rgb(255, 232, 0);");
        $(".operation").attr("style", "color: #4085b7;");
        $(".number").attr("style", "color: #58C554;");
        $(".text").attr("style", "color: white;");

        $(".sortable-code").attr("style", "color: white;");

        $("ul.output").attr("style", "background-color: rgba(48, 52, 63, 0.9);");
        $(".sortable-code li").attr("style", "background-color: rgba(48, 52, 63, 0.9);");
    }
}

function increaseFont() {
    fontSize = parseFloat(fontSize) * 1.2;
    $(".codeContainer").css("font-size", fontSize);
}

function decreaseFont() {
    fontSize = parseFloat(fontSize) /  1.2;
    $(".codeContainer").css("font-size", fontSize);
}

function resizeCodeContainer() {
    let leftWidth = document.getElementById("tutorialCol").offsetWidth;
    let rightWidth = document.getElementById("right-col").offsetWidth;
    width = window.innerWidth - leftWidth - rightWidth - 10;
    let widthString = "width:" + width + "px";

    let bottomHeight = document.getElementById("editorToolbar").offsetHeight;
    bottomHeight += document.getElementById("percent").offsetHeight + 70;
    height = window.innerHeight - bottomHeight;
    let heightString = "height:" + height + "px";
    let styleString = widthString + ";" + heightString;
    document.getElementById("codeContainer").setAttribute("style", styleString);
}

function reset (sortCode) {
    sortCode = sortCode.replaceAll("&#x27;", "");
    sortCode = sortCode.replaceAll(/\\t/g, "");
    sortCode = sortCode.replace("[", "");
    sortCode = sortCode.replace("]", "");
    sortCode = sortCode.split(',');

    placeholderInd = 0;
    let lists = document.getElementsByTagName('ul');
    for (var i = 0; i < lists.length; ++i) {
        if (lists[i].id.includes("ul-sortable") || lists[i].id == "sortableTrash") {
            //Clear lists
            while (lists[i].firstChild) {
                lists[i].removeChild(lists[i].firstChild);
            }
        }

        //Add placeholders
        if (lists[i].id.includes("ul-sortable") && lists[i].id != "ul-sortableTrash") {
            let placeholder = document.createElement('li');
            placeholder.id = "placeholder" + placeholderInd;
            placeholder.className = "placeholder";
            let text = document.createTextNode("Placeholder");
            placeholder.append(text);

            lists[i].appendChild(placeholder);
            ++placeholderInd;
        }

        //Add lines
        else if (lists[i].id == "ul-sortableTrash") {
            let codelineInd = 0;
            //Loop through sortable lines
            for (var j = 0; j < sortCode.length; ++j) {
                codeline = document.createElement('li');
                codeline.id = "codeline" + codelineInd;
                codeline.draggable = true;
                codeline.setAttribute("ondragstart", "drag(event);");

                text = document.createTextNode(sortCode[j]);
                codeline.append(text);

                lists[i].appendChild(codeline);
                ++codelineInd;

                colorCodeSortable(codeline.id)
            }
        }
    }
}

function allowDrop(event) {
    event.preventDefault();
}
function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}
function drop(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text");

    //Clear placeholders
    let listElements = document.getElementById(event.target.id).getElementsByTagName('li');
    if (listElements.length != 0 && listElements[0].id.includes("placeholder")) {
        while (event.target.firstChild) {
            event.target.removeChild(event.target.firstChild);
            placeholderInd--;
        }
    }

    if (event.target.tagName == "LI") {
        event.target.parentNode.appendChild(document.getElementById(data))
    }
    else {
        event.target.appendChild(document.getElementById(data));
    }

    addPlaceholders();
}

function addPlaceholders() {
    let lists = document.getElementsByTagName('ul');
    for (var i = 0; i < lists.length; ++i) {
        if (lists[i].id.includes("ul-sortable") || lists[i].id == "sortableTrash") {
            if (lists[i].childElementCount == 0) {
                let placeholder = document.createElement('li');
                placeholder.id = "placeholder" + placeholderInd;
                placeholder.className = "placeholder";
                let text = document.createTextNode("Placeholder");
                placeholder.append(text);

                lists[i].appendChild(placeholder);
                ++placeholderInd;
            }
        }
    }
}

function colorCodeText(divID) {
    let code = document.getElementById(divID).textContent;
    code = code.replaceAll(/\\r/g, "");
    code = code.replaceAll(/\\n/g, "<br/>");
    code = code.replaceAll(/\\t/g, "&nbsp&nbsp&nbsp&nbsp");
    document.getElementById(divID).innerHTML = "";

    document.getElementById(divID).innerHTML += "<span class=\"text\"> " + lineNumber + "</span>";
    ++lineNumber;

    let lines = code.split(";");
    for (var i = 0; i < lines.length; ++i) {
        let words = lines[i].split(" ");
        for (var j = 0; j < words.length; j++) {
            if (words[j].includes("then")) {
                document.getElementById(divID).innerHTML += "<span class=\"keyword\"> " + words[j] + "</span>";
                continue;
            }

            if (words[j].includes("else")) {
                document.getElementById(divID).innerHTML += "<span class=\"keyword\"> " + words[j] + "</span>";
                continue;
            }

            if (words[j].trim() == "<br/>") {
                continue;
            }
            let breakCount = words[j].split("<br/>").length - 1;
            words[j] = words[j].replaceAll("<br/>", "");

            if (lineNumber >= 10) {
                words[j] = words[j].replace("&nbsp", "");
            }

            for (var breaks = 0; breaks < breakCount; ++breaks) {
                document.getElementById(divID).innerHTML += "<span class=\"text\"><br/>" + lineNumber + "</span>";
                ++lineNumber;
            }

            if (keywords.includes(words[j].replaceAll("<br/>", "").replaceAll("&nbsp", ''))) {
                if (words[j].includes("Procedure")) {
                    let ind = words[j].indexOf('Procedure');
                    document.getElementById(divID).innerHTML += "<span class=\"keyword\"> " + words[j].substring(0, ind + 9) + "<br/></span>";

                    document.getElementById(divID).innerHTML += "<span class=\"text\">" + lineNumber + "</span>";
                    ++lineNumber;
                    document.getElementById(divID).innerHTML += "<span class=\"keyword\">" + words[j].substring(ind + 9, words[j].length) + "</span>";
                    
                }

                else {
                    document.getElementById(divID).innerHTML += "<span class=\"keyword\"> " + words[j] + "</span>";
                }
            }

            else if (operations.includes(words[j].replaceAll("<br/>", "").replaceAll("&nbsp", ''))) {
                document.getElementById(divID).innerHTML += "<span class=\"operation\"> " + words[j] + " </span";
            }

            else if (/\d/.test(words[j])) {
                for (var k = 0; k < words[j].length; ++k) {
                    if (words[j][k] >= '0' && words[j][k] <= '9') {
                        document.getElementById(divID).innerHTML += "<span class=\"number\">" + words[j][k] + "</span>";
                    }

                    else {
                        document.getElementById(divID).innerHTML += "<span class=\"text\">" + words[j][k] + "</span>";
                    }
                }
            }

            else {
                document.getElementById(divID).innerHTML += "<span class=\"text\"> " + words[j] + "</span>";
            }
        }
        if (divID == "firstSetCode") {
            let numSpaces = lines[i].split("&nbsp").length - 1;
            if (numSpaces != 0) {
                parsonsSpaces = "";
                for (var spaces = 0; spaces < numSpaces; ++spaces) {
                    parsonsSpaces += "&nbsp";
                }
            }
        }

        if (lines[i] != "" && !lines[i].includes("do") && !lines[i].includes("else") && !lines[i].includes("then") && lines[i].trim() != "<br/>" && lines[i].trim().length != 0) {
            document.getElementById(divID).innerHTML += "<span class=\"text\">;</span>";
        }
    }
}

function colorCodeSortable(listID, isMultiConfirms) {
    let codeLine = document.getElementById(listID).innerHTML;
    document.getElementById(listID).innerHTML = "";
    if (isMultiConfirms) {
        codeLine = codeLine.replace(/\\t/g, "");
        codeLine = codeLine.trim().split(" ");
        for (var i = 0; i < codeLine.length; ++i) {
            if (keywords.includes(codeLine[i].trim())) {
                document.getElementById(listID).innerHTML += "<span class=\"keyword\">" + codeLine[i] + "</span>";
            }

            else if (codeLine[i].trim().includes("end;")) {
                document.getElementById(listID).innerHTML += "<span class=\"keyword\">end</span>";
                document.getElementById(listID).innerHTML += "<span class=\"text\">;</span>"; 
            }

            else {
                for (var j = 0; j < codeLine[i].length; ++j) {
                    if (operations.includes(codeLine[i][j])) {
                        document.getElementById(listID).innerHTML += "<span class=\"operation\">" + codeLine[i][j] + "</span>";
                    }

                    else if (/\d/.test(codeLine[i][j])) {
                        document.getElementById(listID).innerHTML += "<span class=\"number\">" + codeLine[i][j] + "</span>";
                    }

                    else {
                        document.getElementById(listID).innerHTML += "<span class=\"text\">" + codeLine[i][j] + "</span>";
                    }
                }
            }
            
            document.getElementById(listID).innerHTML += "<span class=\"text\"> </span>";
        }
    }

    else {
        codeLine = codeLine.split("</span>");
        for (var i = 0; i < codeLine.length; ++i) {
            codeLine[i] = codeLine[i].substring(codeLine[i].indexOf(">") + 1, codeLine[i].indexOf(">") + codeLine.length + 5);
            if (keywords.includes(codeLine[i].trim())) {
                document.getElementById(listID).innerHTML += "<span class=\"keyword\">" + codeLine[i] + "</span>";
            }

            else if (operations.includes(codeLine[i].trim())) {
                document.getElementById(listID).innerHTML += "<span class=\"operation\">" + codeLine[i] + "</span>";
            }

            else if (/\d/.test(codeLine[i])) {
                document.getElementById(listID).innerHTML += "<span class=\"number\">" + codeLine[i] + "</span>";
            }

            else {
                document.getElementById(listID).innerHTML += "<span class=\"text\">" + codeLine[i] + "</span>";
            }
        }
    }
}
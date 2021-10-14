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
        organizedCode.forEach((item, index) => {
            let nextAnswer = "";
            nextAnswer = nextAnswer + $('span', item).text();
            nextAnswer = nextAnswer + '\n';
            answers.push(nextAnswer);
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
                answers.splice(index + 1, 0, commentArr[commentInd]);
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

        answers = [];
        for (var i = 0; i < sortables.length; ++i) {
            for (var j = 0; j < sortables[i].childNodes.length; ++j) {
                answers.push(sortables[i].childNodes[j].innerText);
            }
        }

        comments = comments.replaceAll("&#x27;", "");
        comments = comments.replace("[", "");
        comments = comments.replace("]", "");
        let commentArr = comments.split(',');
        let commentInd = 0;

        answers.forEach((element, index) => {
            if (answers[index].includes("While") || answers[index].includes("For")) {
                answers.splice(index + 1, 0, commentArr[commentInd]);
                commentInd++;
            }
        })

        confirms = confirms.replaceAll("&#x27;", "");
        confirms = confirms.replaceAll(/\\t/g, "");
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
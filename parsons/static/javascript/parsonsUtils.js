function getParsonsFeedback (event, setCode, parson) {
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

        let totalAnswerLen = 0;
        for (var i = 0; i < answers.length; ++i) {
            totalAnswerLen = totalAnswerLen + answers[i].length;
        }

        let breakLoop = false;
        let studentCode = "";
        for (var i = 0; i < setCode.length - 10 && !breakLoop; ++i) {
            for (var j = 0; j < answers.length; ++j) {
                if (setCode.substring(i, i + answers[j].length).trim() == answers[j].trim()) {
                    studentCode = setCode.substring(0, i - 1);
                    for (var k = 0; k < answers.length; ++k) {
                        studentCode = studentCode + answers[k];
                        i = i + answers[k].length;
                    }
                    studentCode = studentCode + "\n" + "\n" + setCode.substring(i + 10, setCode.length);

                    breakLoop = true;
                    break;
                }
            }
        }

        studentCode = studentCode.replace("&gt;", ">");
        studentCode = studentCode.replace("&lt;", "<");

        console.log(setCode);
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
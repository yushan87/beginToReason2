/*
    Take the output of all the "processing" steps of the verifier, and combine
    it with the output of the "complete" step. The result is an object with two
    fields: overall and lines. overall tells you if all the VCs proved. lines is
    an array of objects with two fields each, lineNum and status. If there are
    multiple VCs on one line, then it only says the line is proven if all of
    the VCs on that line are proven.
*/
function mergeVCsAndLineNums(provedList, lineNums) {
    var overall = "success";
    var lines = {};

    for (var vc of lineNums) {
        if (provedList[vc.vc] != "success") {
            overall = "failure";
        }

        if (lines[vc.lineNum] != "failure") {
            lines[vc.lineNum] = provedList[vc.vc];
        }
    }

    // Convert from hashtable to array
    var lineArray = [];
    for (var entry of Object.entries(lines)) {
        lineArray.push({
            lineNum: entry[0],
            status: entry[1]
        });
    }

    return {
        overall: overall,
        lines: lineArray
    };
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

    return JSON.stringify(json);
}


function decode(data) {
    var regex1 = new RegExp("%20", "g");
    var regex2 = new RegExp("%2B", "g");
    var regex3 = new RegExp("<vcFile>(.*)</vcFile>", "g");
    var regex4 = new RegExp("\\n", "g");

    var content = decodeURIComponent(data);
    content = content.replace(regex1, " ");
    content = content.replace(regex2, "+");
    content = content.replace(regex3, "$1");
    content = decodeURIComponent(content);
    content = decodeURIComponent(content);
    content = content.replace(regex4, "");

    var obj = JSON.parse(content);

    return obj;
}

function verify(code) {
    var vcs = {};
    var ws = new WebSocket("wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project");

    //opening
    ws.on("open", () => {
        ws.send(encode(code));
    });

    ws.on("message", (message) => {
        message = JSON.parse(message);
        if (message.status == "error" || message.status == "") {
            ws.close();
        } else if (message.status == "processing") {
            var regex = new RegExp("^Proved");
            if (regex.test(message.result.result)) {
                vcs[message.result.id] = "success";
            } else {
                vcs[message.result.id] = "failure";
            }
        } else if (message.status == "complete") {
            var lineNums = decode(message.result);
            var lines = mergeVCsAndLineNums(vcs, lineNums.vcs);

            ws.close();
        }
    });
}

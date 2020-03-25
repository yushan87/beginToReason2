/* global createEditor */

var markers = [];

/**
 * addMarker puts a highlight on important lines of code that are being checked
 * */
function addMarker(lineNum, status) {
    if (status == "success") {
        markers.push(createEditor.session.addMarker(new Range(lineNum - 1, 0, lineNum, 0), "vc_proved"));
    } else {
        markers.push(createEditor.session.addMarker(new Range(lineNum - 1, 0, lineNum, 0), "vc_failed"));
    }
}

/**
 * adds a marker for each line in parameter "lines"
 * */
function addLines(lines) {
    removeMarkers();
    for (var line of lines) {
        addMarker(line.lineNum, line.status);
    }
}

/**
 * remove marker for each marker in markers
 * */
function removeMarkers() {
    for (var marker of markers) {
        createEditor.session.removeMarker(marker);
    }

    markers = [];
}

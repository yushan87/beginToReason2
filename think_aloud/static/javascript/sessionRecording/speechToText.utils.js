/* global sessionId */
/* global postPartialTranscript */
/*eslint no-empty-function: "error"*/
let recognition = null; // Stores the recognition object
let currentTranscript = ""; // Stores the transcribed text starting from the last upload to server
let tempTranscript = ""; // Stores the transcript that is being uploaded to the server
let recognitionCapable = false; // Indicates whether user's browser supports webkitSpeechRecognition
let recognitionOn = false; // Indicates whether recognition is "supposed" to be on or off

/**
 * The main function for setting and running everything related to SpeechToText
 */
function transcribeAudio() {
    if (!("webkitSpeechRecognition" in window)) {
        setBrowserCompatibility(false);
        return;
    }
    setBrowserCompatibility(true);
    setupRecognition();
    startRecognition();
    setupTranscriptUploading();
}

/**
 * Sets an interval of 30 seconds to upload transcribed text.
 */
function setupTranscriptUploading() {
    // upload transcript every 30 seconds
    setInterval(function () {
        if (sessionId) {
            tempTranscript = currentTranscript;
            currentTranscript = "";
            handlePostPartialTranscript(sessionId, tempTranscript);
        }
    }, 30000);
}

/**
 * Calls an API function to upload a transcript and handles errors by retrying in 3 seconds.
 * @param {string} id - Session ID that is returned by API
 * @param {string} transcript - Transcribed text
 */
function handlePostPartialTranscript(id, transcript) {
    postPartialTranscript(id, transcript).then(
        function (response) {
            if (response.status === "success") {
                tempTranscript = ""; // Reset the temporary value
            } else {
                setTimeout(() => handlePostPartialTranscript(id, transcript), 3000); // retry posting a transcript in 3 seconds if failed
            }
        }
    ).catch(function (error) {
        setTimeout(() => handlePostPartialTranscript(id, transcript), 3000); // retry posting a transcript in 3 seconds  if failed
    });
}

/**
 * Starts recognition and set flags
 */
function startRecognition() {
    recognition.start();
    recognitionOn = true;
}

/**
 * Stops recognition and sets all the flags
 */
function stopRecognition() {
    recognition.stop();
    recognitionOn = false;
}

/**
 * Creates and configures the recognition object
 */
function setupRecognition() {
    let SpeechRecognition = SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = "en-US";
    recognition.maxAlternatives = 1; // TODO: test other values
    onStart();
    onResult();
    onEnd();
    onError();
}

/**
 * Sets the browser compatability flag
 * @param {boolean} isCompatible
 */
function setBrowserCompatibility(isCompatible) {
    recognitionCapable = isCompatible;
}

/**
 * Adds new transcript to the main transcript variable
 * @param {string} transcript - New transcript
 * @param {boolean} isFinal - Flag whether the transcript is final or interim
 */
function updateSpeechRecognitionResult(transcript, isFinal) {
    if (isFinal) {
        currentTranscript = currentTranscript += " " + transcript;
    }
}

/**
 * Sets the function that will run in "onresult" event of recognition
 */
function onResult() {
    recognition.onresult = function (event) {
        if (!event.results) {
            return;
        }
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                updateSpeechRecognitionResult(event.results[i][0].transcript, true);
            } else {
                updateSpeechRecognitionResult(event.results[i][0].transcript, false);
            }
        }
    };
}

/**
 * Sets the function that will run in "onresult" event of recognition
 */
function onEnd() {
    recognition.onend = function () {
        if (recognitionOn) {
            recognition.start();
        }
    };
}

/**
 * Sets the function that will run in "onstart" event of recognition
 */
function onStart() {
    /* eslint-disable */
    recognition.onstart = function () {
    };
    /* eslint-enable */
}

/**
 * Sets the function that will run in "onerror" event of recognition
 */
function onError() {
    /* eslint-disable */
    recognition.onerror = function (event) {
    };
    /* eslint-enable */
}

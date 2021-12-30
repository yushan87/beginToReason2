/* global generateSessionId postPartialTranscript */
/* eslint no-empty-function: "error" */

let recognitionObject = null; // Stores the recognition object
let currentTranscript = ""; // Stores the transcribed text starting from the last upload to server
let tempTranscript = ""; // Stores the transcript that is being uploaded to the server
let recognitionCapable = false; // Indicates whether user's browser supports webkitSpeechRecognition
let recognitionOn = false; // Indicates whether recognition is "supposed" to be on or off
let speechRecognitionUniqueId = "";

/**
 * The main function for setting and running everything related to SpeechToText
 */
function transcribeAudio(userId, lessonNumber, lessonName) {
    if (!("webkitSpeechRecognition" in window)) {
        setBrowserCompatibility(false);
        return;
    }
    setBrowserCompatibility(true);
    speechRecognitionUniqueId = generateSessionId(userId, lessonNumber, lessonName);
    setupRecognition();
    startRecognition();
    setupTranscriptUploading();
}

/**
 * Sets an interval of 30 seconds to upload transcribed text.
 */
function setupTranscriptUploading() {
    // upload transcript every 10 seconds
    setInterval(function () {
        if (speechRecognitionUniqueId) {
            tempTranscript = currentTranscript;
            currentTranscript = "";
            handlePostPartialTranscript(speechRecognitionUniqueId, tempTranscript);
        }
    }, 10000);
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
    recognitionObject.start();
    recognitionOn = true;
}

/**
 * Stops recognition and sets all the flags
 */
function stopRecognition() {
    recognitionObject.stop();
    recognitionOn = false;
}

/**
 * Creates and configures the recognition object
 */
function setupRecognition() {
    // let SpeechRecognitionType = SpeechRecognition || window.webkitSpeechRecognition;
    let SpeechRecognitionType = window.webkitSpeechRecognition;
    recognitionObject = new SpeechRecognitionType();
    recognitionObject.continuous = true;
    recognitionObject.interimResults = false;
    recognitionObject.lang = "en-US";
    recognitionObject.maxAlternatives = 1; // TODO: test other values
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
    recognitionObject.onresult = function (event) {
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
    recognitionObject.onend = function () {
        if (recognitionOn) {
            recognitionObject.start();
        }
    };
}

/**
 * Sets the function that will run in "onstart" event of recognition
 */
function onStart() {
    /* eslint-disable */
    recognitionObject.onstart = function () {
    };
    /* eslint-enable */
}

/**
 * Sets the function that will run in "onerror" event of recognition
 */
function onError() {
    /* eslint-disable */
    recognitionObject.onerror = function (event) {
    };
    /* eslint-enable */
}

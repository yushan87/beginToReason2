/*** Start of Global variables ***/
const VIDEO_FRAGMENT_LENGTH = 10000; // Stores the length of a video fragment
let blobCounter = -1; // Stores the current number of a video fragment, used for enumerating video fragments
let currentSessionRecordingId = null; // Session ID returned by API, used for identifying this specific session in transcripts and screen recordings
let currentUserId = ''; // Current user ID


// let activeUploads = 0; // Counts the current number of active uploads
let activeUploads = {
    count: 0,
    aListener: function (val) {
    },
    set a(val) {
        this.count = val;
        this.aListener(val);
    },
    get a() {
        return this.count;
    },
    registerListener: function (listener) {
        this.aListener = listener;
    }
};

let mediaStream = null; // Holds the mediaStream object
let mediaRecorder = null; // Holds the mediaRecorder object
let recordingState = false;

// Timestamps for marking the beginning and ending of the current attempt
let currentAttemptStartTime;
let currentAttemptEndTime;

let currentAttemptCount = 0;

let currentSessionRecordingLessonIndex = -1, currentSessionRecordingLessonName = 'undefined';

/*** End of Global variables ***/

/**
 * Saves ID from the API response
 * @param {Object} response - API response with a session ID
 */
function saveIdCallback(response) {
    if (currentSessionRecordingId === null && "id" in response) {
        currentSessionRecordingId = response.id;
    }
}

/**
 * Runs after a partial upload of a screen recording
 * @param {boolean} uploadSuccessful - Flag whether the upload was successful.
 */
function partialUploadCallback(uploadSuccessful) {
    if (uploadSuccessful) {
        activeUploads.count--; // decrement one successful upload
    }
}

/**
 * Handles new available fragment of a recording by uploading it to the server
 * @param {Blob} blob - New blob
 */
function onDataAvailable(blob) {
    blobCounter++;
    activeUploads.count++;
    // API request body
    const data = {
        ...(currentSessionRecordingId && {"uniqueID": currentSessionRecordingId + "-blob-" + blobCounter}), // eslint-disable-line
        video: blob
    };
    savePartialRecordingAPI(data, saveIdCallback, partialUploadCallback);
}

/**
 * Acquires audio and screen media from user, binds audio to the screen recording and resolves in a MediaStream object
 * @param {boolean} audio - Flag to include audio
 * @param {boolean} screen - Flag to include screen?
 * @returns {Promise<MediaStream>}
 */
async function getMediaStream(audio, screen) {
    const requiredMedia = {
        audio: audio ? {
            echoCancellation: true,
            noiseSuppression: true,
            sampleRate: 44100
        } : false,
        video: screen ? {
            cursor: "always",
            displaySurface: "application"
        } : false
    };
    return new Promise(async function (resolve, reject) { // eslint-disable-line
        try {
            if (screen) {
                const stream = await navigator.mediaDevices.getDisplayMedia({
                    video: requiredMedia.video
                });
                if (audio) {
                    const audioStream = await navigator.mediaDevices.getUserMedia({
                        audio: requiredMedia.audio
                    });

                    audioStream
                        .getAudioTracks()
                        .forEach(audioTrack => stream.addTrack(audioTrack));
                }
                mediaStream = stream;
                resolve(mediaStream);
            } else {
                const stream = await window.navigator.mediaDevices.getUserMedia(requiredMedia);
                mediaStream = stream;
                resolve(mediaStream);
            }
        } catch (error) {
            console.error("error acquiring media devices. error message:", error);
            reject(error);
        }
    });
}

/**
 * Formula: userId + '__' + start_timestamp + '__' + lessonIndex + '__' + lessonName
 * @param {string} userId
 * @param {number} lessonIndex
 * @param {string} lessonName
 */
function generateSessionId(userId, lessonIndex, lessonName) {
    return userId + '__' + Date.now() + '__' + lessonIndex + '__' + lessonName;
}

function resetVariables() {
    currentAttemptCount = 0;
    blobCounter = -1;
    currentSessionRecordingId = null;
    currentAttemptStartTime = 0;
    currentAttemptEndTime = 0;
}

/**
 * Sets up everything that is required for recording a screen and audio.
 * @param {boolean} doAudio - Flag to include audio recording
 * @param {boolean} doScreen - Flag to include screen recording
 * @param {string} userId - User identification for file naming
 * @param lessonIndex
 * @param lessonName
 * @returns {Promise<void>}
 */
async function setupRecording(doAudio, doScreen, userId, lessonIndex, lessonName) {
    resetVariables();
    currentUserId = userId;
    currentSessionRecordingLessonIndex = lessonIndex;
    currentSessionRecordingLessonName = lessonName;
    if (!navigator.mediaDevices) {
        console.log("ERROR: getUserMedia not supported in this browser.");
        return;
    }

    getMediaStream(doAudio, doScreen).then(stream => {
        // console.log('User permitted to share audio');

        currentSessionRecordingId = generateSessionId(userId, lessonIndex, lessonName);
        startNewAttempt();

        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start(VIDEO_FRAGMENT_LENGTH);
        recordingState = true;

        // Uploads the remaining recording
        mediaRecorder.onStop = function (e) {
            onDataAvailable(e.data);
        };

        // Uploads the recording collected during the last period of VIDEO_FRAGMENT_LENGTH
        mediaRecorder.ondataavailable = function (e) {
            onDataAvailable(e.data);
            // download(e.data);
        };

        mediaRecorder.onerror = function (e) {
            console.error("error recording media: ", e);
        };
    });
}

/**
 * Stops MediaRecorder recording
 */
function stopRecording() {
    mediaRecorder.stop();
    // resetVariables();
    recordingState = false;
}

/**
 * Downloads a passed blob in the user's browser. Only used for debugging
 * @param blobData
 */
function download(blobData) {
    const url = window.URL.createObjectURL(blobData);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'test.webm';
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 100);
}

function completeCurrentAttempt(attemptIsSuccessful, errorReason, solutionEntered, code) {
    // capture attempt ending time
    currentAttemptEndTime = Date.now();

    solutionEntered = solutionEntered ? solutionEntered : '';

    handlePostPerAtteptDataRequest(currentSessionRecordingId, currentUserId, attemptIsSuccessful, currentAttemptCount, errorReason,
        solutionEntered, code, currentSessionRecordingLessonIndex, currentSessionRecordingLessonName, currentAttemptEndTime, currentAttemptEndTime);

    if (!attemptIsSuccessful) {
        startNewAttempt();
    } else {
        // end a session because this attempt was successfull
        stopRecording();
    }
}

function startNewAttempt() {
    // set a new start timestamp
    currentAttemptStartTime = Date.now();

    // increment the current attempt count
    currentAttemptCount++;

    // reset other variables
    currentAttemptEndTime = 0;
}

/**
 * Calls an API function to upload per-attempt data and handles errors by retrying in 3 seconds.
 * @param sessionId
 * @param userId
 * @param attemptIsSuccessful
 * @param attemptCount
 * @param errorReason
 * @param solutionEntered
 * @param code
 * @param lessonIndex
 * @param lessonName
 * @param startTimestamp
 * @param endTimestamp
 */
function handlePostPerAtteptDataRequest(sessionId, userId, attemptIsSuccessful, attemptCount, errorReason, solutionEntered, code, lessonIndex, lessonName, startTimestamp, endTimestamp) {
    postPerAttemptData(sessionId, userId, attemptIsSuccessful, attemptCount, errorReason, solutionEntered, code, lessonIndex, lessonName, startTimestamp, endTimestamp).then(
        function (response) {
            if (response.status === "Success") {
                // Good!
            } else {
                setTimeout(() => handlePostPerAtteptDataRequest(sessionId, userId, attemptIsSuccessful, attemptCount, errorReason, solutionEntered, code, lessonIndex,
                    lessonName, startTimestamp, endTimestamp), 3000); // retry posting data in 3 seconds if failed
            }
        }
    ).catch(function (error) {
        setTimeout(() => handlePostPerAtteptDataRequest(sessionId, userId, attemptIsSuccessful, attemptCount, errorReason, solutionEntered, code, lessonIndex,
            lessonName, startTimestamp, endTimestamp), 3000); // retry posting a transcript in 3 seconds  if failed
    });
}
/* global savePartialRecordingAPI */
const VIDEO_FRAGMENT_LENGTH = 30000; // Stores the length of a video fragment
let blobCounter = -1; // Stores the current number of a video fragment, used for enumerating video fragments
let sessionId = null; // Session ID returned by API, used for identifying this specific session in transcripts and screen recordings
let activeUploads = 0; // Counts the current number of active uploads
let mediaStream = null; // Holds the mediaStream object
let mediaRecorder = null; // Holds the mediaRecorder object

/**
 * Saves ID from the API response
 * @param {Object} response - API response with a session ID
 */
function saveIdCallback(response) {
    if (sessionId === null && "id" in response) {
        sessionId = response.id;
    }
}

/**
 * Runs after a partial upload of a screen recording
 * @param {boolean} uploadSuccessful - Flag whether the upload was successful.
 */
function partialUploadCallback(uploadSuccessful) {
    if (uploadSuccessful) {
        activeUploads--; // decrement one successful upload
    }
}

/**
 * Handles new available fragment of a recording by uploading it to the server
 * @param {Blob} blob - New blob
 */
function onDataAvailable(blob) {
    blobCounter++;
    activeUploads++;
    // API request body
    const data = {
        ...(sessionId && {"uniqueID": sessionId + "-blob-" + blobCounter}), // eslint-disable-line
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
        video: {
            cursor: "always",
            displaySurface: "application"
        }
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
 * Sets up everything that is required for recording a screen and audio.
 * @returns {Promise<void>}
 */
async function setupRecording() {
    if (!navigator.mediaDevices) {
        console.log("ERROR: getUserMedia not supported in this browser.");
        return;
    }

    getMediaStream(true, true).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start(VIDEO_FRAGMENT_LENGTH);

        mediaRecorder.onStop = function (e) {
            // TODO: upload the remaining recording when stopped. When is it stopped?
        };

        mediaRecorder.ondataavailable = function (e) {
            onDataAvailable(e.data);
        };

        mediaRecorder.onerror = function (e) {
            console.error("error recording media: ", e);
        };
    });
}

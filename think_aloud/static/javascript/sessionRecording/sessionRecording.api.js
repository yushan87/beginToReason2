const API_ENDPOINT = "https://d2lztt9qntb11c.cloudfront.net"; // Stores the current configuration of API
// const API_ENDPOINT = 'http://socratiusapi-dev.us-west-2.elasticbeanstalk.com/';
const SAVE_PARTIAL_RECORDING_API = "/think-aloud-session/save-partial-recording"; // Stores partial recording upload path in API
const SAVE_PARTIAL_TRANSCRIPT_API = "/begin-to-reason-functions/save-partial-transcript"; // Stores partial transcript upload path in API
const SAVE_PER_ATTEMPT_DATA_API = "/think-aloud-session/save-attempt-data"; // Stores per attempt data

/**
 * Uploads a recording fragment by first requesting an signed upload to S3 request from API and then calling an upload function.
 * @param {{video: Blob, uniqueID?: string}} params - Parameters for upload
 * @param {function} saveId - Callback to save a session ID
 * @param {function} handleUploadStatusChange - Callback to run after the upload is complete.
 */
function savePartialRecordingAPI(params, saveId, handleUploadStatusChange) {
    const url = API_ENDPOINT + SAVE_PARTIAL_RECORDING_API;
    const data = {
        ...("uniqueID" in params && {"uniqueID": params.uniqueID}), // eslint-disable-line
    };

    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 204) {
                const response = JSON.parse(xhr.response);
                if (response.statusCode == 200) {
                    uploadFile(params.video, response.fields, response.url,
                        handleUploadStatusChange);
                    saveId(response);
                } else {
                    handleUploadStatusChange(false);
                }
            } else {
                handleUploadStatusChange(false);
            }
        }
    };
    xhr.send(JSON.stringify(data));
}

/**
 * Uploads a file to an S3 bucket
 * @param {Blob} file - Recording fragment blob
 * @param {Object} s3fields - S3 Fields returned from API
 * @param {string} s3url - URL to s3 bucket
 * @param {function} callback - Callback to run after the upload is complete.
 */
function uploadFile(file, s3fields, s3url, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", s3url);

    let postData = new FormData();
    for (let key in s3fields) {
        postData.append(key, s3fields[key]);
    }

    postData.append("file", file);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 204) {
                callback(true);
            } else {
                console.error("Could not upload file.");
                callback(false);
            }
        }
    };
    xhr.send(postData);
}

/**
 * Uploads an attempt related data
 * @param {string}  sessionId
 * @param {string}  userId
 * @param {boolean} attemptIsSuccessful
 * @param {number}  attemptCount
 * @param {string}  errorReason
 * @param {string}  solutionEntered
 * @param {string}  code
 * @param {number}  lessonIndex
 * @param {string}  lessonName
 * @param {number}  startTimestamp
 * @param {number}  endTimestamp
 */
function postPerAttemptData(sessionId, userId, attemptIsSuccessful, attemptCount, errorReason, solutionEntered, code, lessonIndex, lessonName, startTimestamp, endTimestamp) {
    return postRequest(API_ENDPOINT + SAVE_PER_ATTEMPT_DATA_API,
        {
            sessionId,
            userId,
            attemptIsSuccessful,
            attemptCount,
            errorReason,
            solutionEntered,
            code,
            lessonIndex,
            lessonName,
            startTimestamp,
            endTimestamp
        });
}

/**
 * Uploads a partial transcript
 * @param {string} sessionId
 * @param {string} transcript
 */
function postPartialTranscript(sessionId, transcript) {
    return postRequest(API_ENDPOINT + SAVE_PARTIAL_TRANSCRIPT_API,
        {
            sessionId,
            transcript
        });
}

/**
 * GET request helper
 * @param {string} url
 */
function getRequest(url) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open("GET", url);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200 || xhr.status === 204) {
                    resolve(JSON.parse(xhr.response));
                } else {
                    reject(xhr.statusText);
                }
            }
        };
        xhr.send();
    });
}

/**
 * GET request helper
 * @param {string} url - Request URL
 * @param {Object} body - Request body
 */
function postRequest(url, body) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200 || xhr.status === 204) {
                    resolve(JSON.parse(xhr.response));
                } else {
                    reject(xhr.statusText);
                }
            }
        };
        xhr.send(JSON.stringify(body));
    });
}

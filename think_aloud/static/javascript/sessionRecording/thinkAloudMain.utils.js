/* global completeCurrentAttempt recognitionOn recordingState setupRecording stopRecognition transcribeAudio */

function initThinkAloudFunctions(doAudio, doScreen, doTranscription, userId, lessonNumber, lessonName) {
    if (doAudio || doScreen) {
        setupRecording(doAudio, doScreen, userId, lessonNumber, lessonName); // for recording a session
    }

    if (doTranscription) {
        transcribeAudio(userId, lessonNumber, lessonName);
    }
}

function closeThinkAloudFunctions(attemptIsSuccessful, errorReason, solutionEntered, code) {
    if (recordingState) {
        completeCurrentAttempt(attemptIsSuccessful, errorReason, solutionEntered, code);
    }

    if (recognitionOn) {
        stopRecognition();
    }
}

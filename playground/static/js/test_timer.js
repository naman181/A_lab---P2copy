
// var startTime = new Date().getTime();
// var timer = setInterval(function () {
//    var currentTime = new Date().getTime();
//    var timeElapsed = Math.floor((currentTime - startTime) / 1000);
//    var timeRemaining = '{{ time_limit }}' - timeElapsed;
//    document.getElementById('time_remaining').innerText = timeRemaining;
//    document.getElementById('time_taken').value = timeElapsed; // Update the time_taken value

//    if (timeRemaining <= 0) {
//      clearInterval(timer);
//      document.forms[0].submit(); // Auto-submit the form when time runs out
//    }
// }, 1000);
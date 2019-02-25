window.onload = function (e) {
    user_count = document.getElementById("user_count").value;
    group_count = document.getElementById("group_count").value;
    console.log(user_count)
    animateValue("user", user_count, 1);
    animateValue("group", group_count, 1);
};

function animateValue(id, end, duration) {
    var current = 0;
    var increment = end > 0? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / end));
    var obj = document.getElementById(id);
    var timer = setInterval(function() {
        current += increment;
        obj.innerHTML = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
};
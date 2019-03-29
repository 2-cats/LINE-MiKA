window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    document.getElementById("line_user_id").value = data.context.userId;
    document.getElementById("comment_line_user_id").value = data.context.userId;
}
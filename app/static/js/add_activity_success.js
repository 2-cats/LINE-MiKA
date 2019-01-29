window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    document.getElementById('closewindowbutton').addEventListener('click', function () {
        liff.closeWindow();
    });
}

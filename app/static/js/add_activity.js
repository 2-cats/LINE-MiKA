window.onload = function (e) {
    checkTime();
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    document.getElementById("line_user_id").value = data.context.userId;
}


function checkTime(){
    $("#end").change(function () {
        var startDate = document.getElementById("start").value;
        var endDate = document.getElementById("end").value;

        if ((Date.parse(startDate) > Date.parse(endDate))) {

            $("#endHelper").append("<p>結束日期小於開始日期</p>");

            $("#endHelper p").css('color', 'red')
            document.getElementById("end").value = "";
        }else{
            $("#endHelper p").remove()
        }
    });
     $("#start").change(function () {
        var startDate = document.getElementById("start").value;
        var endDate = document.getElementById("end").value;

        if ((Date.parse(startDate) > Date.parse(endDate))) {

            $("#endHelper1").append("<p>開始日期大於結束日期</p>");

            $("#endHelper1 p").css('color', 'red')
            document.getElementById("start").value = "";
        }else{
            $("#endHelper1 p").remove()
        }
    });
}

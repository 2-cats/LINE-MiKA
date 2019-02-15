window.onload = function (e) {
    showGroupLink();
    checkTime();
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    document.getElementById("line_user_id").value = data.context.userId;
}

function showGroupLink(){
    $('#public-click').click(function() {
        if( $(this).is(':checked')) {
            $("#group-link").show();
            $("#group_link_form").prop('required',true);
        } else {
            $("#group-link").hide();
            $("#group_link_form").prop('required',false);
        }
    });
}

function checkTime(){
    $("#end").change(function () {
        var startDate = document.getElementById("start").value;
        var endDate = document.getElementById("end").value;
    
        if ((Date.parse(startDate) > Date.parse(endDate))) {
            $("#endHelper p").remove()
            $("#endHelper").append("<p>結束日期小於開始日期</p>");
            $("#endHelper p").css('color', 'red')
            document.getElementById("end").value = "";
        }else{
            $("#endHelper p").remove()
        }
    });
}
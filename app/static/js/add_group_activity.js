window.onload = function (e) {
    showGroupLink();
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
            $("group_link_form").prop('required',true);
        } else {
            $("#group-link").hide();
            $("group_link_form").prop('required',false);
        }
    });
}
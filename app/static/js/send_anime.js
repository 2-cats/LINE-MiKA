window.onload = function (e) {
    lightbox();
};

function lightbox(){
    $("#lightbox").fancybox({
        buttons : [
            'download',
            'thumbs',
            'close'
        ]
    });
}
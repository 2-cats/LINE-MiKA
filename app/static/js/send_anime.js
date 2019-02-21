window.onload = function (e) {
    showCard();
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

function showCard(){
    var showCardAnime = anime({
        targets: '#card-img',
        scaleX: [
            {
                value: [0, 340],
                duration: 1200,
                delay: 1500
            }
        ],
        scaleY: [
            {
                value: [0, 180],
                duration: 1200,
                delay: 1500
            }
        ]
      });
};
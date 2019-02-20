window.onload = function (e) {
    bouncingBall();
};

function bouncingBall(){
    var bouncingBall = anime({
        targets: '#card-img',
        scaleX: [
            {
                value: [0, 340],
                duration: 1200,
                delay: 1200
            }
        ],
        scaleY: [
            {
                value: [0, 180],
                duration: 1200,
                delay: 1200
            }
        ]
      });
};
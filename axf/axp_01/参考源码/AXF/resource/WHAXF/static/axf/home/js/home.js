$(function () {

    initTopSwiper();

    initSwiperMenu();

})


function initTopSwiper() {
    var swiper = new Swiper("#topSwiper",{
        pagination: ".swiper-pagination",
        loop: true,
        autoplay: 3000
    })
}


function initSwiperMenu() {
    var swiper = new Swiper("#swiperMenu",{
        slidesPerView:3
    })
}
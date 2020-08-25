$(function () {

    $(".not_login").click(function () {

        window.open("/axf/userlogin/", target="_self");

    })

    $("#not_payed").click(function () {

        window.open('/axf/orderlist/', target="_self");

    })

})